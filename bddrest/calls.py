from urllib.parse import urlencode, parse_qs
import re
import json

from webtest import TestApp

from .types import WsgiApp


URL_PARAMETER_PATTERN = re.compile('/(?P<key>\w+):\s?(?P<value>\w+)')
CONTENT_TYPE_PATTERN = re.compile('(\w+/\w+)(?:;\s?charset=(.+))?')


class Serializable:
    data_attributes = []

    def __init__(self, **kwargs):
        for name in self.data_attributes:
            if name in kwargs:
                setattr(self, name, kwargs[name])

    def to_dict(self):
        result = {}
        for name in self.data_attributes:
            value = getattr(self, name)

            if value is None:
                continue

            if hasattr(value, 'to_dict'):
                value = value.to_dict()

            result[name] = value

        return result


class Response(Serializable):
    data_attributes = [
        'headers', 'status', 'body'
    ]
    content_type = None
    encoding = None
    status = None
    status_code = None
    status_text = None
    headers = None
    body = None

    def __init__(self, status, headers, **kwargs):
        super(Response, self).__init__(status=status, headers=headers, **kwargs)

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


class HttpCall(Serializable):
    data_attributes = [
        'title', 'url', 'verb', 'url_parameters', 'form', 'headers', 'as_', 'query', 'description', 'form', 'response'
    ]
    response: Response = None

    def __init__(self, title: str, url='/', verb='GET', url_parameters: dict=None, form: dict=None,
                 content_type: str=None, headers: list=None, as_: str=None, query: dict=None, description: str=None,
                 response=None):

        if content_type:
            headers = headers or []
            headers.append(('Content-Type', content_type))

        if URL_PARAMETER_PATTERN.search(url):
            if url_parameters is None:
                url_parameters = {}

            for k, v in URL_PARAMETER_PATTERN.findall(url):
                url_parameters[k] = v
                url = re.sub(f'{k}:\s?\w+', f':{k}', url)

        super().__init__(
            title=title,
            url=url,
            verb=verb,
            url_parameters=url_parameters,
            form=form,
            content_type=content_type,
            headers=headers,
            as_=as_,
            query={
                k: v[0] if len(v) == 1 else v for k, v in parse_qs(query).items()} if isinstance(query, str) else query,
            description=description,
            response=Response(**response) if response and not isinstance(response, Response) else response
        )

    def invoke(self):
        raise NotImplementedError()

    def ensure(self):
        if self.response is None:
            self.invoke()

    def copy(self, **kwargs):
        call_data = self.to_dict()
        call_data.update(kwargs)
        return self.__class__(**call_data)


class WsgiCall(HttpCall):

    def __init__(self, application: WsgiApp, title: str, extra_environ: dict=None, **kwargs):
        self.application = application
        self.extra_environ = extra_environ
        super().__init__(title, **kwargs)

    def invoke(self):
        url = f'{self.url}?{urlencode(self.query)}' if self.query else self.url
        kwargs = dict(
            expect_errors=True,
            extra_environ=self.extra_environ,
            headers=self.headers,
            # Commented for future usages by pylover
            # upload_files=upload_files,
        )
        if self.form:
            kwargs['params'] = self.form
        # noinspection PyProtectedMember
        response = TestApp(self.application)._gen_request(self.verb, url, **kwargs)
        self.response = Response(response.status, [(k, v) for k, v in response.headers.items()], body=response.body)

    def copy(self, **kwargs):
        return super().copy(application=self.application, **kwargs)
