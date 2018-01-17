import functools

from .helpers import ObjectProxy
from .models import Composer, Call, When, Story


__version__ = '0.1.0-planning.1'


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
