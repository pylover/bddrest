import io
import json

from ..helpers import querystring_encode
from .helpers import loststr


class CURL:

    def __init__(self, path, form, query, authorization, verb='GET',
                 content_type='text/plain', headers=[], nerds_readable=None,
                 multipart=None, json=None):

        self._path = path
        self._query = query
        self._form = form
        self._headers = headers
        self._multipart = multipart
        self.verb = verb
        self.content_type = content_type
        self.authorization = authorization
        self.nerds_readable = nerds_readable
        self._json = json

    def __repr__(self):
        return ' '.join(self.parts)

    def compile_argument(self, k, v):
        s = '' if self.nerds_readable else ' '
        return f'{k}{s}{v}'

    @property
    def headers(self):
        header_parts = []
        for header in self._headers:
            header_parts.append(self.compile_argument('-H', f'"{header}"'))

        return ' '.join(header_parts)

    @property
    def form(self):
        form_parts = []
        if self._form:
            for k, value in self._form.items():
                for v in value:
                    form_parts.append(
                        self.compile_argument('-F', f'"{k}={v}"'))

        return ' '.join(form_parts)

    @property
    def json(self):
        if self._json:
            return f'--data \'{json.dumps(self._json)}\''

    @property
    def multipart(self):
        multipart_parts = []
        if self._multipart:
            for k, v in self._multipart.items():
                if isinstance(v, io.BytesIO):
                    multipart_parts.append(
                        self.compile_argument('-F', f'"{k}=@<path/to/file>"')
                    )
                else:
                    multipart_parts.append(
                        self.compile_argument('-F', f'"{k}={v}"')
                    )

        return ' '.join(multipart_parts)

    @property
    def query(self):
        return querystring_encode(self._query)

    @property
    def full_path(self):
        query = f'?{self.query}' if self.query else ''
        return f'"{self._path}{query}"'

    @property
    def parts(self):
        parts = ['curl']
        if self.verb != 'GET':
            parts.append(self.compile_argument('-X', self.verb))

        if self.form:
            parts.append(self.form)

        if self.multipart:
            parts.append(self.multipart)

        if self.json:
            parts.append(self.json)

        if self.headers:
            parts.append(self.headers)

        if self.content_type:
            parts.append(self.compile_argument(
                '-H',
                f'"Content-Type: {self.content_type}"'
            ))

        if self.authorization:
            parts.append(self.compile_argument(
                '-H',
                '"Authorization: $TOKEN"'
            ))

        parts.append('--')
        parts.append(self.full_path)
        return parts

    @classmethod
    def from_call(cls, call):
        return cls(
            path=cls.serialize_path(call.path, call.path_parameters),
            query=call.query,
            form=call.form,
            verb=call.verb,
            content_type=call.content_type,
            authorization=call.authorization,
            headers=[f'{k}: {loststr(v)}' for k, v in call.headers or []],
            multipart=call.multipart,
            json=call.json,
        )

    @classmethod
    def serialize_path(cls, path, path_parameters):
        path_part = []

        for part in path.split('/'):
            if part.startswith(':'):
                part = path_parameters[part[1:]]

            path_part.append(part)

        return f'$URL{"/".join(path_part)}'
