
class CURL:
    def __init__(
        self,
        url,
        form,
        query,
        authorization,
        verb='GET',
        content_type='text/plain',
        headers=[],
        nerds_readable=False
    ):
        self._url = url
        self._query = query
        self._form = form
        self._headers = headers
        self.verb = verb
        self.content_type = content_type
        self.authorization = authorization
        self.nerds_readable = nerds_readable

    def __repr__(self):
        return ' '.join(self.parts)

    def compile_argument(self, k, v):
        s = self.nerds_readable and '' or ' '
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
        for k, v in self._form.items():
            form_parts.append(self.compile_argument('-F', f'"{k}={v}"'))

        return ' '.join(form_parts)

    @property
    def query(self):
        query_parts = []
        for k, v in self._query.items():
            query_parts.append(f'{k}={v}')

        return '&'.join(query_parts)

    @property
    def full_path(self):
        return f'"{self._url}?{self.query}"'

    @property
    def parts(self):
        parts = ['curl']
        parts.append(self.compile_argument('-X', self.verb))
        parts.append(self.form)
        parts.append(self.headers)
        parts.append(
            self.compile_argument('-H', f'"Content-Type: {self.content_type}"')
        )
        parts.append(
            self.compile_argument('-H', f'"Authorization: {self.authorization}"')
        )
        parts.append('--')
        parts.append(self.full_path)
        return parts

#    @classmethod
#    def from_call(cls, call: Call) -> 'CURL':
#        raise NotImplementedError
