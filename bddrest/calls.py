from pymlconf import ConfigDict

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
    def __init__(self, application: WsgiApp, **kwargs):
        self.application = application
        super().__init__(kwargs)
