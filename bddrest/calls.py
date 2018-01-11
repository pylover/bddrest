from pymlconf import ConfigDict
from webtest import TestApp

from .types import WsgiApp


class Call(ConfigDict):
    def invoke(self):
        raise NotImplementedError()

    def ensure(self):
        if self.response is not None:
            return
        self.invoke()


class HttpCall(Call):
    @property
    def status(self):
        raise NotImplementedError()

    def invoke(self):
        raise NotImplementedError()


class WsgiCall(HttpCall):
    response = None

    def __init__(self, application: WsgiApp, **kwargs):
        self.application = TestApp(application)
        super().__init__(kwargs)

    def invoke(self):
        self.response = self.application.request(
            self.url,
            method=self.verb,
            expect_errors=True,
        )

