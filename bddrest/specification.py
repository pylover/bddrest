from typing import Any
import io

import yaml

from .calls import HttpCall
from .contexts import Context
from .proxy import ObjectProxy


class Story(Context):
    def __init__(self, call: HttpCall):
        call.ensure()
        self.calls = [call]

    @property
    def call(self):
        return self.calls[-1]

    def push(self, call: HttpCall):
        self.calls.append(call)

    def to_dict(self):
        return dict(
            given=self.calls[0].to_dict(),
            calls=[c.to_dict() for c in self.calls[1:]]
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
    new_call = story.call.copy(title=title, response=None, **kwargs)
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
