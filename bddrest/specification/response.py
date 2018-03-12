import re
import json as jsonlib

from .headerset import HeaderSet


CONTENT_TYPE_PATTERN = re.compile('(\w+/\w+)(?:;\s?charset=(.+))?')


class Response:
    content_type = None
    encoding = None
    body = None

    def __init__(self, status, headers, body=None, json=None):
        self.status = status
        self.headers = HeaderSet(headers) if headers is not None else None
        if json:
            self.body = jsonlib.dumps(json).encode()
            # FIXME: enable it after HeaderSet is implemented.
            # self.headers.append('Content-Type: application/json;charset=utf-8')
        elif body:
            self.body = body.encode() if not isinstance(body, bytes) else body

        status_parts = status.split(' ')
        self.status_code, self.status_text = \
            int(status_parts[0]), ' '.join(status_parts[1:])

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
            status=self.status
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


