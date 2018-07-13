
from ..proxy import ObjectProxy
from ..specification import FirstCall, AlteredCall, Call

from .story import Story
from .given import Given


story = ObjectProxy(Given.get_current)
response = ObjectProxy(lambda: story.response)


def when(*args, **kwargs):
    return story.when(*args, **kwargs)


