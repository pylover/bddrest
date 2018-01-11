from typing import Iterable, Union, Callable

from pymlconf.proxy import ObjectProxy

from .calls import Call
from .contexts import Context


class Given(Context):
    def __init__(self, call: Call):
        self.calls = [call]

    @property
    def current_call(self):
        return self.calls[-1]


class CurrentStory(ObjectProxy):
    def __init__(self):
        super().__init__(Given.get_current)


class When:
    def __init__(self, **kwargs):
        old_call = CurrentStory.current_call
        call = old_call.copy()
        call.merge(kwargs)
        call.ensure()


class Assert:
    pass


class Then:
    def __init__(self, asserts: Iterable[Union[Assert, Callable]]):
        for criteria in asserts:
            criteria()


class ReturnValueProxy:
    pass


story = CurrentStory()
