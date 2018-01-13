from urllib.parse import urlencode
import re

from webtest import TestApp

from .types import WsgiApp


URL_PARAMETER_PATTERN = re.compile('/(?P<key>\w+):\s?(?P<value>\w+)')


class HttpCall:
    def __init__(self, title, url='/', verb='GET', url_parameters=None, form=None,
                 content_type=None, headers=None, as_=None, query=None, description=None):
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

    def __init__(self, application: WsgiApp, title, **kwargs):
        self.application = application
        super().__init__(title, **kwargs)

    def merge(self, other):
        if 'url' in other:
            url = other['url']
            del other['url']
            self.set_url(url)
        return super().merge(other)

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
        url = f'{self.url}?{urlencode(query)}' if query else self.url
        response = TestApp(self.application)._gen_request(self.verb, url, **kwargs)
        members = ['status', 'status_code', 'json', 'body', 'headers', 'content_type']
        self.merge(dict(response={k: getattr(response, k) for k in members if hasattr(response, k)}))
