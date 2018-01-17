import functools

from .helpers import ObjectProxy
from .models import Composer, Call, When


__version__ = '0.1.0-planning.0'


story = ObjectProxy(Composer.get_current)
response = ObjectProxy(lambda: story.current_call.response)


@functools.wraps(Call)
def given(application, *args, **kwargs):
    if args and isinstance(args[0], Call):
        call = args[0]
    else:
        call = Call(*args, **kwargs)
    return Composer(application, call)


def when(*args, **kwargs):
    story.when(*args, **kwargs)


def then(*args, **kwargs):
    story.then(*args, **kwargs)


and_ = then
