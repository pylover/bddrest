
from .helpers import ObjectProxy
from .specification import Call, RestApi, ModifiedCall, VerifyError
from .authoring import Story, ComposingMixin, When, ComposingCall
from .exceptions import InvalidUrlParametersError, ValidationError

__version__ = '0.4.0a2'


story = ObjectProxy(Story.get_current)
response = ObjectProxy(lambda: story.current_call.response)


def given(application, *args, **kwargs):
    return Story(application, *args, **kwargs)


def when(*args, **kwargs):
    story.when(*args, **kwargs)


def then(*args, **kwargs):
    story.then(*args, **kwargs)


and_ = then
