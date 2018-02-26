
from .helpers import ObjectProxy
from .specification import Call, RestApi, ModifiedCall, VerifyError
from .authoring import Given, ComposingMixin, When, ComposingCall
from .exceptions import IncompleteUrlParametersError

__version__ = '0.3.1a1.dev4'


story = ObjectProxy(Given.get_current)
response = ObjectProxy(lambda: story.current_call.response)


def given(application, *args, **kwargs):
    return Given(application, *args, **kwargs)


def when(*args, **kwargs):
    story.when(*args, **kwargs)


def then(*args, **kwargs):
    story.then(*args, **kwargs)


and_ = then
