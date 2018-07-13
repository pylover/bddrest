import yaml

from .context import Context
from .documentary import Documenter, MarkdownFormatter
from .proxy import ObjectProxy
from .specification import FirstCall, AlteredCall, Call


class Story:
    _yaml_options = dict(default_style=False, default_flow_style=False)

    def __init__(self, base_call, calls=None):
        self.base_call = base_call
        self.calls = calls or []

    def to_dict(self):
        return dict(
            base_call=self.base_call.to_dict(),
            calls=[c.to_dict() for c in self.calls]
        )

    @classmethod
    def from_dict(cls, data):
        base_call = FirstCall(**data['base_call'])
        return cls(
            base_call,
            calls=[
                AlteredCall(base_call, **d)
                for d in data['calls']
            ] if data.get('calls') else None
        )

    def dump(self, file):
        data = self.to_dict()
        yaml.dump(data, file, **self._yaml_options)

    def dumps(self):
        data = self.to_dict()
        return yaml.dump(data, **self._yaml_options)

    def verify(self, application):
        self.base_call.verify(application)
        for c in self.calls:
            c.verify(application)

    @classmethod
    def load(cls, file):
        data = yaml.load(file)
        return cls.from_dict(data)

    @classmethod
    def loads(cls, string):
        data = yaml.load(string)
        return cls.from_dict(data)

    def validate(self):
        self.base_call.validate()
        for call in self.calls:
            call.validate()

    def document(self, outfile, formatter_factory=MarkdownFormatter):
        documenter = Documenter(formatter_factory)
        documenter.document(self, outfile)

    @property
    def title(self):
        return self.base_call.title


class Given(Story, Context):
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
        base_call = FirstCall(*args, **kwargs)
        base_call.conclude(application)
        super().__init__(base_call)

    @property
    def current_call(self) -> Call:
        if self.calls:
            return self.calls[-1]
        else:
            return self.base_call

    def when(self, title, **kwargs):
        new_call = AlteredCall(self.base_call, title, **kwargs)
        new_call.conclude(self.application)
        self.calls.append(new_call)
        return new_call

    def __enter__(self):
        return super().__enter__()

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

    @property
    def response(self):
        if self.current_call is None:
            return None
        return self.current_call.response


story = ObjectProxy(Given.get_current)
response = ObjectProxy(lambda: story.response)


def when(*args, **kwargs):
    return story.when(*args, **kwargs)

