
from ..proxy import ObjectProxy
from ..specification import FirstCall, AlteredCall, Call

from .story import Story
from .given import Given
from .manipulation import Manipulator, Append, Remove, Update, when


story = ObjectProxy(Given.get_current)
response = ObjectProxy(lambda: story.response)
status = ObjectProxy(lambda: response.status)

