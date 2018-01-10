from pymlconf import ConfigDict


class Call(ConfigDict):
    def invoke(self):
        raise NotImplementedError()


class HttpCall(Call):
    def verify(self, backend):
        raise NotImplementedError()

    @property
    def status(self):
        raise NotImplementedError()

    def invoke(self):
        raise NotImplementedError()


class WsgiCall(HttpCall):
    def __init__(self, application, *args, **kwargs):
        self.application = application
        super().__init__(*args, **kwargs)
