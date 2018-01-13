from typing import Any
import io

from pymlconf.proxy import ObjectProxy
import yaml

from .calls import Call
from .contexts import Context


class Story(Context):
    def __init__(self, call: Call):
        call.ensure()
        self.calls = [call]

    @property
    def call(self):
        return self.calls[-1]

    def push(self, call: Call):
        self.calls.append(call)

    def to_dict(self):
        return dict(given=self.calls[0], calls=self.calls[1:])

    def dump(self, file):
        data = self.to_dict()
        yaml.dump(data, file, default_flow_style=False)

    def dumps(self):
        file = io.BytesIO()
        self.dump(file)
        return file.getvalue()


class Given(Story):
    pass


class CurrentStory(ObjectProxy):
    def __init__(self):
        super().__init__(Given.get_current)


story = CurrentStory()


class When:
    def __init__(self, title, **kwargs):
        old_call = story.call
        call = old_call.copy()
        del call['response']
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
    @staticmethod
    def __get_current_response():
        return story.call.response

    def __init__(self):
        super().__init__(self.__get_current_response)


response = CurrentResponse()
