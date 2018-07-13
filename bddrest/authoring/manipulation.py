import abc

from .given import Given


class Manipulator(metaclass=abc.ABCMeta):
    def __init__(self, *args, **kwargs):
        self.list_diff = args
        if not isinstance(self.list_diff, list):
            self.list_diff = list(self.list_diff)

        self.dict_diff = kwargs

    @abc.abstractmethod
    def apply(self):
        pass


class Add(Manipulator):
    def apply(self, container):
        clone = container.copy()
        if isinstance(clone, dict):
            clone.update(self.dict_diff)
        else:
            clone += self.list_diff
        return clone


def when(*args, **kwargs):
    story = Given.get_current()

    args = [
        a.apply(story.base_call) if isinstance(a, Manipulator) else a
        for a in args
    ]

    kwargs = {
        k: a.apply(getattr(story.base_call, k)) if isinstance(a, Manipulator) else a
        for k, a in kwargs.items()
    }

    return story.when(*args, **kwargs)


