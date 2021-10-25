import re
import sys
from abc import ABCMeta, abstractmethod
from urllib.parse import urlparse, urlencode

from ..connectors import WSGIConnector
from ..exceptions import CallVerifyError, InvalidUrlParametersError
from ..helpers import normalize_query_string
from ..response import Response


URL_PARAMETER_VALUE_PATTERN = r'[ \w\d_-]+'
URL_PARAMETER_PATTERN = \
    re.compile(rf'/(?P<key>\w+):\s?(?P<value>{URL_PARAMETER_VALUE_PATTERN})')


class Call(metaclass=ABCMeta):

    def __init__(self, title=None, description=None, response=None):
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

        if self.body is not None:
            # Raw data
            result['body'] = self.body
        elif self.form is not None:
            # URL-Encodded form
            result['form'] = self.form
        elif self.json is not None:
            # Json payload
            result['json'] = self.json
        elif self.multipart is not None:
            # Multipart form
            result['multipart'] = self.multipart

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
        # i[1:].strip() for i in re.findall(r':[ \w]+', self.url))
        required_parameters = set(
            i[1:] for i in re.findall(
                fr':\s?{URL_PARAMETER_VALUE_PATTERN}', self.url)
        )

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

        if url is None:
            return None, None, None

        # Parsing the querystrings if available
        if parsedurl.query:
            query = normalize_query_string(parsedurl.query)

        url = parsedurl.path
        if URL_PARAMETER_PATTERN.search(url):
            for k, v in URL_PARAMETER_PATTERN.findall(url):
                url_parameters[k] = v
                url = re.sub(
                    rf'{k}:\s?{URL_PARAMETER_VALUE_PATTERN}', rf':{k}',
                    url
                )

        return url, url_parameters if url_parameters else None, query

    def add_header_if_not_exists(self, headers, key, value):
        for k, v in headers:
            if k.lower() == key.lower():
                headers.remove((k, v))
        headers.append((key, value))

    def invoke(self, application) -> Response:
        url = self.url
        if self.url_parameters:
            for k, v in self.url_parameters.items():
                url = url.replace(f':{k}', str(v))

        url = f'{url}?{urlencode(self.query)}' if self.query else url

        headers = self.headers.copy() if self.headers else []
        if self.content_type:
            self.add_header_if_not_exists(
                headers,
                'Content-Type',
                self.content_type
            )

        if self.authorization:
            self.add_header_if_not_exists(
                headers,
                'authorization',
                self.authorization
            )

        request_params = dict(
            environ=self.extra_environ,
            headers=headers,
        )

        if self.body:
            request_params['body'] = self.body
        elif self.form:
            request_params['form'] = self.form
        elif self.json:
            request_params['json'] = self.json
        elif self.multipart:
            request_params['multipart'] = self.multipart

        response = WSGIConnector(application).request(
            self.verb,
            url,
            **request_params
        )

        if 500 <= response.status < 600:
            if response.content_type == 'application/json':
                out = response.json['stackTrace']
            else:
                out = response.text

            print(out, file=sys.stderr)

        return response

    def verify(self, application):
        response = self.invoke(application)
        if self.response != response:
            raise CallVerifyError()

    def conclude(self, application):
        if self.response is None:
            self.validate()
            self.response = self.invoke(application)

    def __repr__(self):
        result = f'{self.verb} {self.url} HTTP/1.1'

        if self.headers is not None:
            header = [': '.join(h) for h in self.headers]
            result = f'{result}\n{header}'

        if self.body is not None:
            result = f'{result}\n{self.body}'
        elif self.form is not None:
            result = f'{result}\n{self.form}'
        elif self.json is not None:
            result = f'{result}\n{self.json}'
        elif self.multipart is not None:
            result = f'{result}\n{self.multipart}'

        return result

    @property
    @abstractmethod
    def verb(self) -> str:  # pragma: no cover
        pass

    @verb.setter
    @abstractmethod
    def verb(self, value):  # pragma: no cover
        pass

    @property
    @abstractmethod
    def url(self) -> str:  # pragma: no cover
        pass

    @url.setter
    @abstractmethod
    def url(self, value):  # pragma: no cover
        pass

    @property
    @abstractmethod
    def url_parameters(self) -> dict:  # pragma: no cover
        pass

    @url_parameters.setter
    @abstractmethod
    def url_parameters(self, value):  # pragma: no cover
        pass

    @property
    @abstractmethod
    def headers(self):  # pragma: no cover
        pass

    @headers.setter
    @abstractmethod
    def headers(self, value):  # pragma: no cover
        pass

    @property
    @abstractmethod
    def form(self) -> dict:  # pragma: no cover
        pass

    @form.setter
    @abstractmethod
    def form(self, value):  # pragma: no cover
        pass

    @property
    @abstractmethod
    def json(self) -> dict:  # pragma: no cover
        pass

    @json.setter
    @abstractmethod
    def json(self, value):  # pragma: no cover
        pass

    @property
    @abstractmethod
    def multipart(self) -> dict:  # pragma: no cover
        pass

    @multipart.setter
    @abstractmethod
    def multipart(self, value):  # pragma: no cover
        pass

    @property
    @abstractmethod
    def query(self) -> dict:  # pragma: no cover
        pass

    @query.setter
    @abstractmethod
    def query(self, value):  # pragma: no cover
        pass

    @property
    @abstractmethod
    def content_type(self) -> str:  # pragma: no cover
        pass

    @content_type.setter
    @abstractmethod
    def content_type(self, value):  # pragma: no cover
        pass

    @property
    @abstractmethod
    def authorization(self) -> str:  # pragma: no cover
        pass

    @content_type.setter
    @abstractmethod
    def authorization(self, value):  # pragma: no cover
        pass

    @property
    @abstractmethod
    def as_(self) -> str:  # pragma: no cover
        pass

    @as_.setter
    @abstractmethod
    def as_(self, value):  # pragma: no cover
        pass

    @property
    @abstractmethod
    def extra_environ(self) -> dict:  # pragma: no cover
        pass

    @extra_environ.setter
    @abstractmethod
    def extra_environ(self, value):  # pragma: no cover
        pass
