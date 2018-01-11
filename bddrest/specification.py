from pymlconf.proxy import ObjectProxy

from .calls import Call, WsgiCall
from .contexts import Context
from .exceptions import AttributeAssertionError, EqualityAssertionError


class ReturnValueProxy:
    pass


class Story(Context):
    __call_factory__ = Call

    def __init__(self, title, **kwargs):
        if isinstance(title, Call):
            self.calls = [title]
        else:
            self.calls = [Call(title=title, **kwargs)]

    @property
    def current_call(self):
        return self.calls[-1]


class CurrentStory(ObjectProxy):
    def __init__(self):
        super().__init__(Story.get_current)


class RestApiStory(Story):
    def __init__(self, title, url, **kwargs):
        super().__init__(self.__call_factory__(title, url=url, **kwargs))

    def __call_factory__(self, *args, **kwargs):
        raise NotImplementedError()


class WsgiRestApiStory(RestApiStory):

    def __call_factory__(self, *args, **kwargs):
        return WsgiCall(self.application, *args, **kwargs)

    def __init__(self, application, *args, **kwargs):
        self.application = application
        super().__init__(*args, **kwargs)


class When:
    pass


class Then:
    def __init__(self, *args):
        call = CurrentStory.call
        return_value = call.invoke()
        for k, v in kwargs.items():
            if not hasattr(return_value, k):
                raise AttributeAssertionError(return_value, k)

            value = getattr(return_value, k)
            if callable(v):
                v(value)
            elif v == value:
                raise EqualityAssertionError(v, value)
