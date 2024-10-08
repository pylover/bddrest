from ..context import Context
from ..specification import FirstCall, AlteredCall, Call
from .manipulation import Manipulator
from .story import Story


class Given(Story, Context):
    """
    :param application: A WSGI Application to examine.
    :param autodump: A file-like object to write dumped story.
                     Default is `None`, means autodump is disabled by default.
    :param autodoc: A dictionary to pass to :class:`Documenter` and enable
                    auto documentary.


    See :class:`Story` for other arguments.
    """

    def __init__(self, application, *args, autodump=None, autodoc=None,
                 **kwargs):
        self.application = application
        self.autodump = autodump
        self.autodoc = autodoc
        base_call = FirstCall(*args, **kwargs)
        base_call.conclude(application)
        super().__init__(base_call)

    @property
    def current_call(self) -> Call:
        if self.calls:
            return self.calls[-1]
        else:
            return self.base_call

    def when(self, *args, record=True, **kwargs):
        # Checking for list manipulators if any
        # Checking for dictionary manipulators if any
        for k, v in kwargs.items():
            if isinstance(v, Manipulator):
                basevalue = getattr(self.base_call, k)
                if basevalue is None:
                    raise ValueError(f'{k} argument is not given yet')
                clone = getattr(self.base_call, k).copy()
                v.apply(clone)
                kwargs[k] = clone

        new_call = AlteredCall(self.base_call, *args, **kwargs)
        new_call.conclude(self.application)
        if record:
            self.calls.append(new_call)
        return new_call

    def __enter__(self):
        return super().__enter__()

    def __exit__(self, exc_type, exc_value, traceback):
        super().__exit__(exc_type, exc_value, traceback)
        if self.base_call.title is None:
            return

        if self.autodump:
            self.dump(self.autodump)

        if self.autodoc:
            self.document(**self.autodoc)

    @property
    def response(self):
        if self.current_call is None:
            return None
        return self.current_call.response
