import re
import json as jsonlib

from .headerset import HeaderSet


CONTENT_TYPE_PATTERN = re.compile('(\w+/\w+)(?:;\s?charset=(.+))?')


class HTTPStatus:

    def __init__(self, code):
        self.code, self.text = code.split(' ', 1)
        self.code = int(self.code)

    @property
    def fulltext(self):
        return f'{self.code} {self.text}'

    def raise_value_error(self):
        raise ValueError(
            'Cannot compare with string, Use integer instead for all '
            'comparison types except equality'
        )

    def __eq__(self, other):
        if isinstance(other, int):
            return self.code == other

        if isinstance(other, self.__class__):
            other = other.fulltext

        return self.fulltext.casefold() == other.casefold()

    def __gt__(self, other):
        if isinstance(other, int):
            return self.code > other
        self.raise_value_error()

    def __ge__(self, other):
        if isinstance(other, int):
            return self.code >= other
        self.raise_value_error()

    def __lt__(self, other):
        if isinstance(other, int):
            return self.code < other
        self.raise_value_error()

    def __le__(self, other):
        if isinstance(other, int):
            return self.code <= other
        self.raise_value_error()

    def __str__(self):
        return self.fulltext

    def __repr__(self):
        return f'\'{str(self)}\''


class Response:
    content_type = None
    encoding = None
    body = None

    def __init__(self, status, headers, body=None, json=None):
        self.status = HTTPStatus(status)
        self.headers = HeaderSet(headers) if headers is not None else None
        if json:
            self.body = jsonlib.dumps(json).encode()
            # FIXME: enable it after HeaderSet is implemented.
            # self.headers.append('Content-Type: application/json;charset=utf-8')
        elif body:
            self.body = body.encode() if not isinstance(body, bytes) else body

        if headers:
            for k, v in self.headers:
                if k == 'Content-Type':
                    match = CONTENT_TYPE_PATTERN.match(v)
                    if match:
                        self.content_type, self.encoding = match.groups()
                    break

    @property
    def text(self):
        return self.body.decode()

    @property
    def json(self):
        return jsonlib.loads(self.body)

    def to_dict(self):
        result = dict(
            status=str(self.status)
        )
        if self.headers:
            result['headers'] = self.headers.simple

        if self.body:
            if self.content_type == 'application/json':
                result['json'] = self.json
            else:
                result['body'] = self.body.decode()
        return result

    def __eq__(self, other: 'Response'):
        if self.status != other.status or self.headers != other.headers:
            return False

        if self.content_type == 'application/json':
            return self.json == other.json

        return self.body == other.body

