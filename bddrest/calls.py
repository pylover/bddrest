from urllib.parse import urlencode
import re

from pymlconf import ConfigDict
from webtest import TestApp

from .types import WsgiApp


URL_PARAMETER_PATTERN = re.compile('/(?P<key>\w+):\s?(?P<value>\w+)')


class Call(ConfigDict):

    def invoke(self):
        raise NotImplementedError()

    def ensure(self):
        if 'response' in self and self.response is not None:
            return
        self.invoke()

    def copy(self):
        return self.__class__(**self)


class HttpCall(Call):

    def invoke(self):
        raise NotImplementedError()


class WsgiCall(HttpCall):

    def __init__(self, application: WsgiApp, url='/', **kwargs):
        if not isinstance(application, TestApp):
            application = TestApp(application)
        self.application = application
        self.set_url(url)
        super().__init__(kwargs)

    def merge(self, other):
        if 'url' in other:
            url = other['url']
            del other['url']
            self.set_url(url)
        return super().merge(other)

    def set_url(self, url):
        if URL_PARAMETER_PATTERN.search(url):
            url_parameters = dict()
            for k, v in URL_PARAMETER_PATTERN.findall(url):
                url_parameters[k] = v
                url = re.sub(f'{k}:\s?\w+', f':{k}', url)
        else:
            url_parameters = None
        self['url'] = url
        self['url_parameters'] = url_parameters

    def invoke(self):
        kwargs = dict(
            expect_errors=True,
            # Commented for future usages by pylover
            # headers=headers,
            # extra_environ=extra_environ,
            # upload_files=upload_files,
            # content_type=content_type
        )

        if hasattr(self, 'form'):
            kwargs['params'] = self.form

        query = self.get('query')

        url = self.url
        if self.url_parameters:
            for k, v in self.url_parameters.items():
                url = url.replace(f':{k}', str(v))
        url = f'{url}?{urlencode(query)}' if query else url

        response = self.application._gen_request(self.verb, url, **kwargs)
        members = ['status', 'status_code', 'json', 'body', 'headers', 'content_type']
        self.merge(dict(response={k: getattr(response, k) for k in members if hasattr(response, k)}))

    def copy(self):
        return self.__class__(self.application, **self)
