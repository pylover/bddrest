from .specification import Given, When, Story, Call
from .helpers import Context, ObjectProxy
from .types import WsgiApp


class Composer(Story, Context):
    def __init__(self, application: WsgiApp, *args, **kwargs):
        self.application = application
        base_call = Given(*args, **kwargs)
        base_call.conclude(application)
        super().__init__(base_call)

    @property
    def current_call(self) -> Call:
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


composer = ObjectProxy(Composer.get_current)
response = ObjectProxy(lambda: composer.current_call.response)


def given(application, *args, **kwargs):
    return Composer(application, *args, **kwargs)


def when(*args, **kwargs):
    composer.when(*args, **kwargs)


def then(*args, **kwargs):
    composer.then(*args, **kwargs)


and_ = then

