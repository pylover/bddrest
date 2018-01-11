from typing import Union, Callable

from pymlconf.proxy import ObjectProxy

from .calls import Call
from .contexts import Context
from .exceptions import AttributeAssertionError


class Given(Context):
    def __init__(self, call: Call):
        call.ensure()
        self.calls = [call]

    @property
    def call(self):
        return self.calls[-1]

    def push(self, call: Call):
        self.calls.append(call)


class CurrentStory(ObjectProxy):
    def __init__(self):
        super().__init__(Given.get_current)


story = CurrentStory()


class When:
    def __init__(self, **kwargs):
        old_call = CurrentStory.call
        call = old_call.copy()
        call.merge(kwargs)
        call.ensure()
        CurrentStory.push(call)


class Assert:
    def __call__(self):
        raise NotImplementedError()


class Then:
    def __init__(self, *asserts: Union[Assert, Callable]):
        for criteria in asserts:
            criteria()


class CurrentResponse:
    def __getattr__(self, name):
        return AssertAttribute(name)


response = CurrentResponse()


class AssertAttribute(Assert):
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent or story.call.response

    def __call__(self):
        if not hasattr(self.parent, self.name):
            raise AttributeAssertionError(story.call, self.name)

    def __getattr__(self, name):
        return AssertAttribute(name, parent=self)

    # def __eq__(self, other):
