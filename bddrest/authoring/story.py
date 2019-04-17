import yaml

try:
    from yaml import CLoader as Loader

except ImportError:  # pragma: no cover
    from yaml import Loader

from ..documentary import Documenter, MarkdownFormatter
from ..specification import FirstCall, AlteredCall


class Story:
    _yaml_options = dict(default_style=False, default_flow_style=False)

    def __init__(self, base_call, calls=None):
        self.base_call = base_call
        self.calls = calls or []

    def to_dict(self):
        return dict(
            base_call=self.base_call.to_dict(),
            calls=[c.to_dict() for c in self.calls if c.title is not None]
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
        data = yaml.load(file, Loader)
        return cls.from_dict(data)

    @classmethod
    def loads(cls, string):
        data = yaml.load(string, Loader)
        return cls.from_dict(data)

    def validate(self):
        self.base_call.validate()
        for call in self.calls:
            call.validate()

    def document(self, outfile, formatter_factory=MarkdownFormatter, **kw):
        documenter = Documenter(formatter_factory, **kw)
        documenter.document(self, outfile)

    @property
    def title(self):
        return self.base_call.title

