from urllib.parse import urlencode
import re

from webtest import TestApp

from .types import WsgiApp


URL_PARAMETER_PATTERN = re.compile('/(?P<key>\w+):\s?(?P<value>\w+)')


class Response:
    pass


class HttpCall:
    response: Response = None

    def __init__(self, title: str, url='/', verb='GET', url_parameters: dict=None, form: dict=None,
                 content_type: str=None, headers: list=None, as_: str=None, query: dict=None, description: str=None):
        self.description = description
        self.query = query
        self.form = form
        self.url = url
        self.title = title
        self.verb = verb
        self.as_ = as_
        self.headers = headers or []
        self.url_parameters = url_parameters
        if content_type:
            self.headers.append(('Content-Type', content_type))

        if URL_PARAMETER_PATTERN.search(self.url):
            if self.url_parameters is None:
                self.url_parameters = {}

            for k, v in URL_PARAMETER_PATTERN.findall(self.url):
                self.url_parameters[k] = v
                self.url = re.sub(f'{k}:\s?\w+', f':{k}', self.url)

    def invoke(self):
        raise NotImplementedError()


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
        self.response = TestApp(self.application)._gen_request(self.verb, url, **kwargs)
