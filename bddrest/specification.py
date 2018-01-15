from typing import Any
import io

import yaml

from .calls import Call, AlteredCall
from .contexts import Context
from .proxy import ObjectProxy


class Story(Context):
    def __init__(self, call: Call):
        call.ensure()
        self.calls = [call]

    @property
    def call(self) -> Call:
        return self.calls[-1]

    @property
    def base_call(self) -> Call:
        return self.calls[0]

    @property
    def altered_calls(self):
        return self.calls[1:]

    def push(self, call: Call):
        self.calls.append(call)

    def to_dict(self):
        return dict(
            given=self.base_call.to_dict(),
            calls=[c.to_dict() for c in self.altered_calls]
        )

    def dump(self, file):
        data = self.to_dict()
        yaml.dump(data, file, default_style=False, default_flow_style=False)

    def dumps(self):
        file = io.StringIO()
        self.dump(file)
        return file.getvalue()


class Given(Story):
    pass


class CurrentStory(ObjectProxy):
    def __init__(self):
        super().__init__(Given.get_current)


story = CurrentStory()


# noinspection PyPep8Naming
def When(title, **kwargs):
    new_call = AlteredCall(story.base_call, title, **kwargs)
    new_call.ensure()
    story.push(new_call)


# noinspection PyPep8Naming
def Then(*asserts: Any):
    for passed in asserts:
        assert passed is not False


class CurrentResponse(ObjectProxy):
    @staticmethod
    def __get_current_response():
        return story.call.response

    def __init__(self):
        super().__init__(self.__get_current_response)


response = CurrentResponse()
