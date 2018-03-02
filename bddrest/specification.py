import re
import json as jsonlib
from urllib.parse import urlencode

import yaml
from webtest import TestApp

from .helpers import normalize_headers, normalize_query_string
from .exceptions import InvalidUrlParametersError


CONTENT_TYPE_PATTERN = re.compile('(\w+/\w+)(?:;\s?charset=(.+))?')
URL_PARAMETER_VALUE_PATTERN = '[\w\d_-]+'
URL_PARAMETER_PATTERN = re.compile(f'/(?P<key>\w+):\s?(?P<value>{URL_PARAMETER_VALUE_PATTERN})')


class VerifyError(Exception):
    pass


# FIXME: Implement it!
class HeaderSet(set):

    def __init(self, headers):
        # TODO: normalize
        raise NotImplementedError()

    def add(self, item, overwrite=False):
        """
        Error if header exists and overwrite is False.
        :param item:
        :param overwrite:
        :return:
        """
        raise NotImplementedError()


class Response:
    content_type = None
    encoding = None
    body = None

    def __init__(self, status, headers, body=None, json=None):
        self.status = status
        self.headers = normalize_headers(headers)
        if json:
            self.body = jsonlib.dumps(json)
            # FIXME: enable it after HeaderSet is implemented.
            # self.headers.append('Content-Type: application/json;charset=utf-8')
        elif body:
            self.body = body.encode() if not isinstance(body, bytes) else body

        if ' ' in status:
            parts = status.split(' ')
            self.status_code, self.status_text = int(parts[0]), ' '.join(parts[1:])
        else:
            self.status_code = int(status)

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
            result['headers'] = [': '.join(h) for h in self.headers]

        if self.body:
            if self.content_type == 'application/json':
                result['json'] = self.json
            else:
                result['body'] = self.body.decode()
        return result

    def __eq__(self, other: 'Response'):
        if self.status != other.status \
                or self.headers != other.headers:
            return False

        if self.content_type == 'application/json':
            return self.json == other.json

        return self.body == other.body


class Call:
    _response: Response = None
    _url = None
    _headers = None
    _query = None

    def __init__(self, title: str, url='/', verb='GET', url_parameters: dict = None,
                 form: dict = None, content_type: str = None, headers: list = None, as_: str = None, query: dict = None,
                 description: str = None, extra_environ: dict = None, response=None):
        self.title = title
        self.response = response
        self.description = description
        self.extra_environ = extra_environ
        self.url = url
        # the `url_parameters` attribute may be set by the url setter. so we're
        # not going to override it anyway.
        if url_parameters is not None:
            self.url_parameters = url_parameters
        self.verb = verb
        self.form = form
        self.content_type = content_type
        self.headers = headers
        self.as_ = as_
        self.query = query

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url, self.url_parameters = self.extract_url_parameters(value)

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, value):
        self._headers = normalize_headers(value)

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, value):
        self._query = normalize_query_string(value)

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

    def validate_url_parameters(self):
        given_parameters = set(self.url_parameters)
        required_parameters = set(i[1:] for i in re.findall(':\w+', self.url))
        
        if given_parameters != required_parameters:
            raise InvalidUrlParametersError(
                required_parameters,
                given_parameters
            )
        
        for k, v in self.url_parameters.items():
            if not isinstance(v, str):
                self.url_parameters[k] = str(v)

    def validate(self):
        self.validate_url_parameters()

    @staticmethod
    def extract_url_parameters(url):
        url_parameters = {}
        if URL_PARAMETER_PATTERN.search(url):
            for k, v in URL_PARAMETER_PATTERN.findall(url):
                url_parameters[k] = v
                url = re.sub(f'{k}:\s?{URL_PARAMETER_VALUE_PATTERN}', f':{k}', url)
        return url, url_parameters

    def invoke(self, application):
        url = self.url
        if self.url_parameters:
            for k, v in self.url_parameters.items():
                url = url.replace(f':{k}', str(v))

        url = f'{url}?{urlencode(self.query)}' if self.query else url

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
        return Response(response.status, [(k, v) for k, v in response.headers.items()], body=response.body)

    def verify(self, application):
        response = self.invoke(application)
        if self.response != response:
            raise VerifyError()


class ModifiedCall(Call):
    def __init__(self, base_call: Call, title: str, description=None, response=None, url_parameters=None, **diff):
        self.base_call = base_call
        if 'url' in diff:
            diff['url'], diff['url_parameters'] = self.extract_url_parameters(diff['url'])
        if url_parameters:
            diff.setdefault('url_parameters', {})
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


class RestApi:
    _yaml_options = dict(default_style=False, default_flow_style=False)

    def __init__(self, base_call, calls=None):
        self.base_call = base_call
        self.calls = calls or []

    def to_dict(self):
        return dict(
            base_call=self.base_call.to_dict(),
            calls=[c.to_dict() for c in self.calls]
        )

    @classmethod
    def from_dict(cls, data):
        base_call = Call(**data['base_call'])
        return cls(
            base_call,
            calls=[ModifiedCall(base_call, **d) for d in data['calls']] if data.get('calls') else None
        )

    def dump(self, file):
        data = self.to_dict()
        yaml.dump(data, file, **self._yaml_options)

    def dumps(self):
        data = self.to_dict()
        return yaml.dump(data, **self._yaml_options)

    def verify(self, application):
        self.base_call.verify(application)
        for c in self.calls:
            c.verify(application)

    @classmethod
    def load(cls, file):
        data = yaml.load(file)
        return cls.from_dict(data)

    @classmethod
    def loads(cls, string):
        data = yaml.load(string)
        return cls.from_dict(data)

    def validate(self):
        self.base_call.validate()
        for call in self.calls:
            call.validate()
