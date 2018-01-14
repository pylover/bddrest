from urllib.parse import urlencode, parse_qs
import re
import json

from webtest import TestApp

from .types import WsgiApp

URL_PARAMETER_VALUE_PATTERN = '[\w\d_-]+'
URL_PARAMETER_PATTERN = re.compile(f'/(?P<key>\w+):\s?(?P<value>{URL_PARAMETER_VALUE_PATTERN})')
CONTENT_TYPE_PATTERN = re.compile('(\w+/\w+)(?:;\s?charset=(.+))?')
UNCHANGED = 'UNCHANGED'


class Response:
    content_type = None
    encoding = None

    def __init__(self, status, headers, body=None):
        self.status = status
        self.headers = headers
        self.body = body.encode() if not isinstance(body, bytes) else body

        if ' ' in status:
            parts = status.split(' ')
            self.status_code, self.status_text = int(parts[0]), ' '.join(parts[1:])
        else:
            self.status_code = int(status)

        for i in self.headers:
            k, v = i.split(': ') if isinstance(i, str) else i
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
        return json.loads(self.body)

    def to_dict(self):
        result = dict(
            status=self.status
        )
        if self.headers:
            result['headers'] = [': '.join(h) for h in self.headers]

        if self.body:
            result['body'] = self.body.decode()
        return result

class Call:
    _response: Response = None
    verb = NotImplemented
    url = NotImplemented
    url_parameters = NotImplemented
    form = NotImplemented
    content_type = NotImplemented
    headers = NotImplemented
    as_ = NotImplemented
    query = NotImplemented
    description = NotImplemented

    def __init__(self, title: str, response=None):
        self.title = title
        self.response = response

    @property
    def response(self) -> Response:
        return self._response

    @response.setter
    def response(self, v):
        self._response = Response(**v) if v and not isinstance(v, Response) else v

    def invoke(self):
        raise NotImplementedError()

    
class BaseCall(Call):

    def __init__(self, application: WsgiApp, title: str, url='/', verb='GET', url_parameters: dict = None,
                 form: dict = None, content_type: str = None, headers: list = None, as_: str = None, query: dict = None,
                 description: str = None, extra_environ: dict = None, response=None):
        super().__init__(title, response=response)
        self.application = application
        self.extra_environ = extra_environ
        if content_type:
            headers = headers or []
            headers.append(('Content-Type', content_type))

        if URL_PARAMETER_PATTERN.search(url):
            if url_parameters is None:
                url_parameters = {}

            for k, v in URL_PARAMETER_PATTERN.findall(url):
                url_parameters[k] = v
                url = re.sub(f'{k}:\s?{URL_PARAMETER_VALUE_PATTERN}', f':{k}', url)

        self.url = url
        self.verb = verb
        self.url_parameters = url_parameters
        self.form = form
        self.content_type = content_type
        self.headers = self.normalize_headers(headers)
        self.as_ = as_
        self.query = self.normalize_query_string(query)
        self.description = description

    def ensure(self):
        if self.response is None:
            self.invoke()

    def to_dict(self):
        result = dict(
            title=self.title,
            url=self.url,
            verb=self.verb,
        )
        if self.url_parameters is not None:
            result['url_parameters'] = self.url_parameters

        if self.form is not None:
            result['form'] = self.form

        if self.headers is not None:
            result['headers'] = [': '.join(h) for h in self.headers]

        if self.as_ is not None:
            result['as_'] = self.as_

        if self.query is not None:
            result['query'] = self.query

        if self.description is not None:
            result['description'] = self.description

        if self.response is not None:
            result['response'] = self.response.to_dict()

        return result

    def invoke(self):
        # Overriding params using kwargs
        url = f'{self.url}?{urlencode(self.query)}' if self.query else self.url

        request_params = dict(
            expect_errors=True,
            extra_environ=self.extra_environ,
            headers=self.headers,
            # Commented for future usages by pylover
            # upload_files=upload_files,
        )
        if self.form:
            request_params['params'] = self.form
        # noinspection PyProtectedMember
        response = TestApp(self.application)._gen_request(self.verb, url, **request_params)
        self.response = Response(response.status, [(k, v) for k, v in response.headers.items()], body=response.body)

    @staticmethod
    def normalize_headers(headers):
        if headers:
            headers = [h.split(':', 1) if isinstance(h, str) else h for h in headers]
            headers = [(k.strip(), v.strip()) for k, v in headers]
        return headers

    @staticmethod
    def normalize_query_string(, query):
        return {k: v[0] if len(v) == 1 else v for k, v in parse_qs(query).items()} if isinstance(query, str) else query


class AlteredCall(Call):
    def __init__(self, base_call, title: str, verb=UNCHANGED, url_parameters: dict = UNCHANGED, form: dict = UNCHANGED,
                 content_type: str = UNCHANGED, headers: list = UNCHANGED, as_: str = UNCHANGED,
                 query: dict = UNCHANGED, description: str = UNCHANGED, extra_environ: dict = UNCHANGED,
                 response=None):
        super().__init__(title, response)
        self.base_call = base_call
        self.diff = diff = {}
        if verb != UNCHANGED:
            diff['verb'] = verb
            
        if url_parameters != UNCHANGED:
            diff['url_parameters'] = url_parameters

        if form != UNCHANGED:
            diff['form'] = form

        if content_type != UNCHANGED:
            diff['content_type'] = content_type

        if headers != UNCHANGED:
            diff['headers'] = headers

        if as_ != UNCHANGED:
            diff['as_'] = as_

        if query != UNCHANGED:
            diff['query'] = query

        if description != UNCHANGED:
            diff['description'] = description

        if extra_environ != UNCHANGED:
            diff['extra_environ'] = extra_environ

        if verb != UNCHANGED:
            diff['verb'] = verb

