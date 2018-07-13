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


class Append(Manipulator):
    def apply(self, container):
        if isinstance(container, dict):
            for k, v in self.dict_diff.items():
                if k in container:
                    raise ValueError(
                        f'The key: {k} is already exists in the target '
                        f'container. You may use the bddrest.Update object.'
                    )
            container.update(self.dict_diff)
        else:
            container += self.list_diff


class Update(Manipulator):
    def apply(self, container):
        if isinstance(container, dict):
            container.update(self.dict_diff)
        else:
            raise ValueError('Only dict is supported for Update manipulator')


def when(*args, **kwargs):
    story = Given.get_current()

    for k, v in kwargs.items():
        if isinstance(v, Manipulator):
            clone = getattr(story.base_call,k)
            v.apply(clone)
            kwargs[k] = clone

    return story.when(*args, **kwargs)

