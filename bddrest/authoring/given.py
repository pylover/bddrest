from ..context import Context
from ..specification import FirstCall, AlteredCall, Call
from .story import Story
from .manipulation import Manipulator


class Given(Story, Context):
    """
    :param application: A WSGI Application to examine
    :param autodump: A string which indicates the filename to dump the story,
                     or a `callable(story) -> filename` to determine the
                     filename. A file-like object is also accepted.
                     Default is `None`, means autodump is disabled by default.
    :param autodoc: A string which indicates the name of documentation file, or
                     a `callable(story) -> filename` to determine the filename.
                     A file-like object is also accepted.
                     Default is `None`, meana autodoc is disabled by default.
                     Currently only markdown is supprted.
    :param fieldinfo: A callable(resource, verb, fieldname) to provide the
                      field's metadata.
    """

    def __init__(self, application, *args, autodump=None, autodoc=None,
                 fieldinfo=None, **kwargs):
        self.application = application
        self.autodump = autodump
        self.autodoc = autodoc
        self.fieldinfo = fieldinfo
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
            if hasattr(self.autodump, 'write'):
                self.dump(self.autodump)
            else:
                filename = self.autodump(self) if callable(self.autodump) \
                    else self.autodump
                with open(filename, mode='w', encoding='utf-8') as f:
                    self.dump(f)

        if self.autodoc:
            if hasattr(self.autodoc, 'write'):
                self.dump(self.autodoc)
            else:
                filename = self.autodoc(self) if callable(self.autodoc) else \
                    self.autodoc
                with open(filename, mode='w', encoding='utf-8') as f:
                    self.document(f, fieldinfo=self.fieldinfo)

    @property
    def response(self):
        if self.current_call is None:
            return None
        return self.current_call.response

