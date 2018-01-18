import functools

from .helpers import ObjectProxy
from .specification import Call, Story, OverriddenCall, VerifyError
from .authoring import Composer, ComposingMixin, When, ComposingCall


__version__ = '0.2.0-planning.2'


story = ObjectProxy(Composer.get_current)
response = ObjectProxy(lambda: story.current_call.response)


@functools.wraps(Composer)
def given(application, *args, **kwargs):
    return Composer(application, *args, **kwargs)


def when(*args, **kwargs):
    story.when(*args, **kwargs)


def then(*args, **kwargs):
    story.then(*args, **kwargs)


and_ = then
