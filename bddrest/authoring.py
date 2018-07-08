from .helpers import Context, ObjectProxy
from .specification import Given, When, Call
from .story import Story


class Composer(Story, Context):
    """
    :param application: A WSGI Application to examine
    :param autodump: A string which indicates the filename to dump the story, or
                     a `callable(story) -> filename` to determine the filename.
                     A file-like object is also accepted.
                     Default is `None`, means autodump is disabled by default.
    :param autodoc: A string which indicates the name of documentation file, or
                     a `callable(story) -> filename` to determine the filename.
                     A file-like object is also accepted.
                     Default is `None`, meana autodoc is disabled by default.
                     Currently only markdown is supprted.
    """

    def __init__(self, application, *args, autodump=None, autodoc=None, **kwargs):
        self.application = application
        self.autodump = autodump
        self.autodoc = autodoc
        base_call = Given(*args, **kwargs)
        base_call.conclude(application)
        super().__init__(base_call)

    @property
    def current_call(self) -> Call:
        if self.calls:
            return self.calls[-1]
        else:
            return self.base_call

    def when(self, title, **kwargs):
        new_call = When(self.base_call, title, **kwargs)
        new_call.conclude(self.application)
        self.calls.append(new_call)
        return new_call

    def __exit__(self, exc_type, exc_value, traceback):
        super().__exit__(exc_type, exc_value, traceback)
        if self.autodump:
            if hasattr(self.autodump, 'write'):
                self.dump(self.autodump)
            else:
                filename = self.autodump(self) if callable(self.autodump) else self.autodump
                with open(filename, mode='w', encoding='utf-8') as f:
                    self.dump(f)

        if self.autodoc:
            if hasattr(self.autodoc, 'write'):
                self.dump(self.autodoc)
            else:
                filename = self.autodoc(self) if callable(self.autodoc) else self.autodoc
                with open(filename, mode='w', encoding='utf-8') as f:
                    self.document(f)


composer = ObjectProxy(Composer.get_current)
response = ObjectProxy(lambda: composer.current_call.response)
given = Composer


def when(*args, **kwargs):
    return composer.when(*args, **kwargs)

