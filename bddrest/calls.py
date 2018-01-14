from urllib.parse import urlencode, parse_qs
import re
import json

from webtest import TestApp

from .types import WsgiApp

URL_PARAMETER_VALUE_PATTERN = '[\w\d_-]+'
URL_PARAMETER_PATTERN = re.compile(f'/(?P<key>\w+):\s?(?P<value>{URL_PARAMETER_VALUE_PATTERN})')
CONTENT_TYPE_PATTERN = re.compile('(\w+/\w+)(?:;\s?charset=(.+))?')


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


class HttpCall:
    data_attributes = [
        'title', 'url', 'verb', 'url_parameters', 'form', 'headers', 'as_', 'query', 'description', 'form', 'response'
    ]
    response: Response = None

    @staticmethod
    def normalize_headers(headers):
        if headers:
            headers = [h.split(':', 1) if isinstance(h, str) else h for h in headers]
            headers = [(k.strip(), v.strip()) for k, v in headers]
        return headers

    @staticmethod
    def normalize_query_string(, query):
        return {k: v[0] if len(v) == 1 else v for k, v in parse_qs(query).items()} if isinstance(query, str) else query

    def __init__(self, title: str, url='/', verb='GET', url_parameters: dict = None, form: dict = None,
                 content_type: str = None, headers: list = None, as_: str = None, query: dict = None,
                 description: str = None,
                 response=None):

        if content_type:
            headers = headers or []
            headers.append(('Content-Type', content_type))

        if URL_PARAMETER_PATTERN.search(url):
            if url_parameters is None:
                url_parameters = {}

            for k, v in URL_PARAMETER_PATTERN.findall(url):
                url_parameters[k] = v
                url = re.sub(f'{k}:\s?{URL_PARAMETER_VALUE_PATTERN}', f':{k}', url)

        self.title = title
        self.url = url
        self.verb = verb
        self.url_parameters = url_parameters
        self.form = form
        self.content_type = content_type
        self.headers = self.normalize_headers(headers)
        self.as_ = as_
        self.query = self.normalize_query_string(query)
        self.description = description
        self.response = Response(**response) if response and not isinstance(response, Response) else response

    def invoke(self, **kwargs):
        raise NotImplementedError()

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

    def alter(self, title: str, verb=None, url_parameters: dict = None, form: dict = None, content_type: str = None,
              headers: list = None, as_: str = None, query: dict = None, description: str = None, response=None):
        pass


class AlteredCall(HttpCall):
    pass


class WsgiCall(HttpCall):

    def __init__(self, application: WsgiApp, title: str, extra_environ: dict = None, **kwargs):
        self.application = application
        self.extra_environ = extra_environ
        super().__init__(title, **kwargs)

    def invoke(self, **kwargs):
        # Overriding params using kwargs
        url = kwargs.get('url', self.url)
        query = kwargs.get('query', self.query)

        url = f'{url}?{urlencode(query)}' if query else url

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
