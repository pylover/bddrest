from .specification import Call, ModifiedCall, RestApi
from .helpers import Context
from .types import WsgiApp


class ComposingMixin:
    response = None

    def conclude(self: Call, application):
        if self.response is None:
            self.validate()
            self.response = self.invoke(application)


class ComposingCall(Call, ComposingMixin):
    pass


class When(ModifiedCall, ComposingMixin):
    pass


class Story(RestApi, Context):
    def __init__(self, application: WsgiApp, *args, **kwargs):
        self.application = application
        base_call = ComposingCall(*args, **kwargs)
        base_call.conclude(application)
        super().__init__(base_call)

    @property
    def current_call(self) -> ComposingMixin:
        if self.calls:
            return self.calls[-1]
        else:
            return self.base_call

    def when(self, title, **kwargs):
        new_call = When(self.base_call, title, **kwargs)
        new_call.conclude(self.application)
        self.calls.append(new_call)
        return new_call

    def then(self, *asserts):
        self.current_call.conclude(self.application)
        for passed in asserts:
            assert passed is not False
        return self.current_call

