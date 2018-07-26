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
        if not isinstance(container, dict):
            raise ValueError('Only dict is supported for Update manipulator')

        container.update(self.dict_diff)


class Remove(Manipulator):
    def __init__(self, *args):
        super().__init__(*args)

    def apply(self, container):
        if not isinstance(self.list_diff, list):
            raise ValueError('Only list is supported for Remove manipulator')

        for k in self.list_diff:
            if k not in container:
                raise ValueError(f'The key: {k} is not exist in the target')

            if isinstance(container, dict):
                del container[k]
            else:
                container.remove(k)


def when(*args, **kwargs):
    story = Given.get_current()

    for k, v in kwargs.items():
        if isinstance(v, Manipulator):
            clone = getattr(story.base_call, k).copy()
            v.apply(clone)
            kwargs[k] = clone

    return story.when(*args, **kwargs)

