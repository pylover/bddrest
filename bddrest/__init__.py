import functools

from .models import Story, Call, AlteredCall
from .helpers import ObjectProxy

__version__ = '0.1.0-planning.0'


story = ObjectProxy(Story.get_current)
response = ObjectProxy(lambda: story.call.response)


@functools.wraps(Call)
def given(application, *args, **kwargs):
    if isinstance(application, Call):
        call = application
    else:
        call = Call(application, *args, **kwargs)
    return Story(call)


def when(*args, **kwargs):
    story.when(*args, **kwargs)


def then(*args, **kwargs):
    story.then(*args, **kwargs)


and_ = then
