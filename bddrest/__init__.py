
from .helpers import ObjectProxy
from .specification import Call, Story, OverriddenCall, VerifyError
from .authoring import Given, ComposingMixin, When, ComposingCall


__version__ = '0.3.0-planning.2'


story = ObjectProxy(Given.get_current)
response = ObjectProxy(lambda: story.current_call.response)


def given(application, *args, **kwargs):
    return Given(application, *args, **kwargs)


def when(*args, **kwargs):
    story.when(*args, **kwargs)


def then(*args, **kwargs):
    story.then(*args, **kwargs)


and_ = then
