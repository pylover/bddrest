from typing import Any

from pymlconf.proxy import ObjectProxy

from .calls import Call
from .contexts import Context


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
    def __init__(self, title, **kwargs):
        old_call = story.call
        call = old_call.copy()
        kwargs['title'] = title
        call.merge(kwargs)
        call.ensure()
        story.push(call)


class Then:
    def __init__(self, *asserts: Any):
        for passed in asserts:
            assert passed is not False


class And(Then):
    pass


class CurrentResponse(ObjectProxy):
    def __init__(self):
        super().__init__(lambda: story.call.response)


response = CurrentResponse()
