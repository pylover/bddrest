
from ..response import Response, AllResponse
from .alteredcall import AlteredCall


class RepeatCall(AlteredCall):

    def __init__(self, base_call, **kwargs):
        super().__init__(base_call, title=None, **kwargs)

    def invoke(self, application) -> Response:
        responses = [self.base_call.response]
        for k, v in self.diff.items():
            for key, values in v.items():
                for item in values:

                    kwargs = {}
                    clone = getattr(self.base_call, k).copy()
                    clone.update({key: item})
                    kwargs[k] = clone

                    call = AlteredCall(self.base_call, '', **kwargs)
                    call.conclude(application)
                    responses.append(call.response)

        self.response = AllResponse(responses)
        return self.response
