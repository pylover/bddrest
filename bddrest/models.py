import io
import re
import json
from typing import Any
from urllib.parse import urlencode, parse_qs

from webtest import TestApp
import yaml

from .types import WsgiApp
from .helpers import Context


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


class Call:
    _response: Response = None

    def __init__(self, title: str, url='/', verb='GET', url_parameters: dict = None,
                 form: dict = None, content_type: str = None, headers: list = None, as_: str = None, query: dict = None,
                 description: str = None, extra_environ: dict = None, response=None):
        self.title = title
        self.response = response
        self.description = description
        self.extra_environ = extra_environ

        self.url, self.url_parameters = self.extract_url_parameters(url)
        if url_parameters:
            self.url_parameters.update(url_parameters)
        self.verb = verb
        self.form = form
        self.content_type = content_type
        self.headers = self.normalize_headers(headers)
        self.as_ = as_
        self.query = self.normalize_query_string(query)

    @property
    def response(self) -> Response:
        return self._response

    @response.setter
    def response(self, v):
        self._response = Response(**v) if v and not isinstance(v, Response) else v

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

    def ensure(self, application):
        if self.response is None:
            self.invoke(application)

    @staticmethod
    def normalize_headers(headers):
        if headers:
            headers = [h.split(':', 1) if isinstance(h, str) else h for h in headers]
            headers = [(k.strip(), v.strip()) for k, v in headers]
        return headers

    @staticmethod
    def normalize_query_string(query):
        return {k: v[0] if len(v) == 1 else v for k, v in parse_qs(query).items()} if isinstance(query, str) else query

    @staticmethod
    def extract_url_parameters(url):
        url_parameters = {}
        if URL_PARAMETER_PATTERN.search(url):
            for k, v in URL_PARAMETER_PATTERN.findall(url):
                url_parameters[k] = v
                url = re.sub(f'{k}:\s?{URL_PARAMETER_VALUE_PATTERN}', f':{k}', url)
        return url, url_parameters

    def invoke(self, application):
        url = f'{self.url}?{urlencode(self.query)}' if self.query else self.url

        headers = self.headers or []
        if self.content_type:
            headers = [h for h in headers if h[0].lower() != 'content-type']
            headers.append(('Content-Type', self.content_type))

        request_params = dict(
            expect_errors=True,
            extra_environ=self.extra_environ,
            headers=headers,
            # Commented for future usages by pylover
            # upload_files=upload_files,
        )
        if self.form:
            request_params['params'] = self.form

        # noinspection PyProtectedMember
        response = TestApp(application)._gen_request(self.verb, url, **request_params)
        self.response = Response(response.status, [(k, v) for k, v in response.headers.items()], body=response.body)


class When(Call):
    def __init__(self, base_call, title: str, description=None, response=None, url_parameters=None, **diff):
        self.base_call = base_call
        if 'url' in diff:
            diff['url'], diff['url_parameters'] = self.extract_url_parameters(diff['url'])
        if url_parameters:
            diff['url_parameters'].update(url_parameters)
        self.diff = diff

        data = {k: v for k, v in base_call.to_dict().items() if k not in ('response', 'title', 'description')}
        data.update(diff)
        super().__init__(title, description=description, response=response, **data)

    def to_dict(self):
        result = dict(title=self.title)
        result.update(self.diff)

        if self.description is not None:
            result['description'] = self.description

        if self.response is not None:
            result['response'] = self.response.to_dict()

        return result


class Story:
    def __init__(self, base_call, calls=None):
        self.base_call = base_call
        self.calls = calls or []

    def to_dict(self):
        return dict(
            given=self.base_call.to_dict(),
            calls=[c.to_dict() for c in self.calls]
        )

    def dump(self, file):
        data = self.to_dict()
        yaml.dump(data, file, default_style=False, default_flow_style=False)

    def dumps(self):
        file = io.StringIO()
        self.dump(file)
        return file.getvalue()


class Composer(Story, Context):
    def __init__(self, application: WsgiApp, *args, **kwargs):
        self.application = application
        if args and isinstance(args[0], Call):
            base_call = args[0]
        else:
            base_call = Call(*args, **kwargs)
        base_call.ensure(application)
        super().__init__(base_call)

    @property
    def current_call(self) -> Call:
        if self.calls:
            return self.calls[-1]
        else:
            return self.base_call

    def when(self, title, **kwargs):
        new_call = When(self.base_call, title, **kwargs)
        new_call.ensure(self.application)
        self.calls.append(new_call)

    def then(self, *asserts: Any):
        self.current_call.ensure(self.application)
        for passed in asserts:
            assert passed is not False
