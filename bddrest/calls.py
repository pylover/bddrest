from pymlconf import ConfigDict
from webtest import TestApp

from .types import WsgiApp


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

    def __init__(self, application: WsgiApp, **kwargs):
        if not isinstance(application, TestApp):
            application = TestApp(application)
        self.application = application
        super().__init__(kwargs)

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

        response = self.application._gen_request(self.verb, self.url, **kwargs)
        members = ['status', 'status_code', 'json', 'body', 'headers', 'content_type']
        self.merge(dict(response={k: getattr(response, k) for k in members if hasattr(response, k)}))

    def copy(self):
        return self.__class__(self.application, **self)
