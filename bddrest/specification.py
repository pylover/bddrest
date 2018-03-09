import re
import json as jsonlib
from abc import ABCMeta, abstractmethod
from urllib.parse import urlencode, urlparse
from typing import Iterable

import yaml
from webtest import TestApp

from .helpers import normalize_headers, normalize_query_string
from .exceptions import InvalidUrlParametersError, CallVerifyError


CONTENT_TYPE_PATTERN = re.compile('(\w+/\w+)(?:;\s?charset=(.+))?')
URL_PARAMETER_VALUE_PATTERN = '[\w\d_-]+'
URL_PARAMETER_PATTERN = \
    re.compile(f'/(?P<key>\w+):\s?(?P<value>{URL_PARAMETER_VALUE_PATTERN})')


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
            self.body = jsonlib.dumps(json).encode()
            # FIXME: enable it after HeaderSet is implemented.
            # self.headers.append('Content-Type: application/json;charset=utf-8')
        elif body:
            self.body = body.encode() if not isinstance(body, bytes) else body

        if ' ' in status:
            parts = status.split(' ')
            self.status_code, self.status_text = int(parts[0]), ' '.join(parts[1:])
        else:
            self.status_code = int(status)

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


class Call(metaclass=ABCMeta):

    def __init__(self, title, description=None, response=None):
        self.title = title
        self.description = description
        if response is not None and not isinstance(response, Response):
            response = Response(**response)
        self.response = response

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
        required_parameters = set(i[1:] for i in re.findall(':\w+', self.url))
        if not required_parameters and self.url_parameters is None:
            return

        given_parameters = set(self.url_parameters or [])

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
        query = None
        parsedurl = urlparse(url)

        # Parsing the querystrings if available
        if parsedurl.query:
            query = normalize_query_string(parsedurl.query)

        url = parsedurl.path
        if URL_PARAMETER_PATTERN.search(url):
            for k, v in URL_PARAMETER_PATTERN.findall(url):
                url_parameters[k] = v
                url = re.sub(f'{k}:\s?{URL_PARAMETER_VALUE_PATTERN}', f':{k}', url)

        return url, url_parameters if url_parameters else None, query

    def invoke(self, application) -> Response:
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
            raise CallVerifyError()

    def conclude(self, application):
        if self.response is None:
            self.validate()
            self.response = self.invoke(application)

    @property
    @abstractmethod
    def verb(self) -> str:
        pass

    @verb.setter
    @abstractmethod
    def verb(self, value):
        pass

    @property
    @abstractmethod
    def url(self) -> str:
        pass

    @url.setter
    @abstractmethod
    def url(self, value):
        pass

    @property
    @abstractmethod
    def url_parameters(self) -> dict:
        pass

    @url_parameters.setter
    @abstractmethod
    def url_parameters(self, value):
        pass

    @property
    @abstractmethod
    def headers(self) -> Iterable:
        pass

    @headers.setter
    @abstractmethod
    def headers(self, value: Iterable):
        pass

    @property
    @abstractmethod
    def form(self) -> dict:
        pass

    @form.setter
    @abstractmethod
    def form(self, value):
        pass

    @property
    @abstractmethod
    def query(self) -> dict:
        pass

    @query.setter
    @abstractmethod
    def query(self, value):
        pass

    @property
    @abstractmethod
    def content_type(self) -> str:
        pass

    @content_type.setter
    @abstractmethod
    def content_type(self, value):
        pass

    @property
    @abstractmethod
    def as_(self) -> str:
        pass

    @as_.setter
    @abstractmethod
    def as_(self, value):
        pass

    @property
    @abstractmethod
    def extra_environ(self) -> dict:
        pass

    @extra_environ.setter
    @abstractmethod
    def extra_environ(self, value):
        pass


class Given(Call):

    _headers = None
    _url = None
    _url_parameters = None
    _verb = None
    _query = None
    _form = None
    _content_type = None  # FIXME: remove it and use header set to store it.
    _as = None
    _extra_environ = None

    def __init__(self, title: str, url='/', verb='GET', url_parameters: dict = None, form: dict = None,
                 content_type: str = None, headers: list = None, as_: str = None, query: dict = None,
                 description: str = None, extra_environ: dict = None, response: Response=None):
        super().__init__(title, description=description, response=response)

        self.url = url
        # the `url_parameters` and `query` attributes may be set by the url setter. so we're
        # not going to override them anyway.
        if url_parameters is not None:
            self.url_parameters = url_parameters

        if query is not None:
            self.query = query

        self.verb = verb
        self.form = form
        self.content_type = content_type
        self.headers = headers
        self.as_ = as_
        self.extra_environ = extra_environ

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url, self.url_parameters, self.query = self.extract_url_parameters(value)

    @property
    def url_parameters(self):
        return self._url_parameters

    @url_parameters.setter
    def url_parameters(self, value):
        self._url_parameters = value

    @property
    def verb(self):
        return self._verb

    @verb.setter
    def verb(self, value):
        self._verb = value

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
    def content_type(self):
        return self._content_type

    @content_type.setter
    def content_type(self, value):
        self._content_type = value

    @property
    def as_(self):
        return self._as

    @as_.setter
    def as_(self, value):
        self._as = value

    @property
    def extra_environ(self):
        return self._extra_environ

    @extra_environ.setter
    def extra_environ(self, value):
        self._extra_environ = value

    @property
    def form(self):
        return self._form

    @form.setter
    def form(self, value):
        self._form = value


class When(Call):
    def __init__(self, base_call: Given, title: str, description=None, response=None,
                 headers=None, **diff):
        self.base_call = base_call
        super().__init__(title, description=description, response=response)

        if 'url' in diff:
            diff['url'], url_parameters, query = self.extract_url_parameters(diff['url'])
            if 'url_parameters' not in diff:
                diff['url_parameters'] = url_parameters

            if 'query' not in diff:
                diff['query'] = normalize_query_string(query)

        self.diff = diff
        self.headers = headers

    def to_dict(self):
        result = dict(title=self.title)
        result.update(self.diff)

        if self.description is not None:
            result['description'] = self.description

        if self.response is not None:
            result['response'] = self.response.to_dict()

        return result

    def update_diff(self, key, value):
        if not value:
            self.diff.pop(key, None)
        else:
            self.diff[key] = value

    @property
    def url(self):
        return self.diff.get('url', self.base_call.url)

    @url.setter
    def url(self, value):
        url, self.url_parameters, self.query = self.extract_url_parameters(value)
        if url:
            self.diff['url']
        else:
            self.diff.pop('url', None)

    @property
    def url_parameters(self):
        return self.diff.get('url_parameters', self.base_call.url_parameters)

    @url_parameters.setter
    def url_parameters(self, value):
        self.update_diff('url_parameters', value)

    @property
    def verb(self):
        return self.diff.get('verb', self.base_call.verb)

    @verb.setter
    def verb(self, value):
        self.update_diff('verb', value)

    @property
    def headers(self):
        return self.diff.get('headers', self.base_call.headers)

    @headers.setter
    def headers(self, value):
        self.update_diff('headers', normalize_headers(value))

    @property
    def query(self):
        return self.diff.get('query', self.base_call.query)

    @query.setter
    def query(self, value):
        self.update_diff('query', normalize_query_string(value))

    @property
    def content_type(self):
        return self.diff.get('content_type', self.base_call.content_type)

    @content_type.setter
    def content_type(self, value):
        self.update_diff('content_type', value)

    @property
    def as_(self):
        return self.diff.get('as_', self.base_call.as_)

    @as_.setter
    def as_(self, value):
        self.update_diff('as_', value)

    @property
    def extra_environ(self):
        return self.diff.get('extra_environ', self.base_call.extra_environ)

    @extra_environ.setter
    def extra_environ(self, value):
        self.update_diff('extra_environ', value)

    @property
    def form(self):
        return self.diff.get('form', self.base_call.form)

    @form.setter
    def form(self, value):
        self.update_diff('form', value)

