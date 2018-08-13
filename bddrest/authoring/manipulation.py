import abc
from collections import Iterable



class Manipulator(metaclass=abc.ABCMeta):
    def __init__(self, *args, **kwargs):
        self.list_diff = args

        if not isinstance(self.list_diff, list):
            self.list_diff = list(self.list_diff)

        self.dict_diff = kwargs

    @abc.abstractmethod
    def apply(self):
        pass

    def __add__(self, other):
        return CompositeManipulator(self) + other

    def __sub__(self, other):
        return CompositeManipulator(self) - other

    def __or__(self, other):
        return CompositeManipulator(self) | other



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
            return

        if not self.list_diff:
            raise ValueError(
                'Invalid list manipulation value, Use positional argument '
                'instead of keyword arguments'
            )
        container.extend(self.list_diff)


class Update(Manipulator):
    def apply(self, container):
        if not isinstance(container, dict):
            raise ValueError('Only dict is supported for Update manipulator')

        container.update(self.dict_diff)


class Remove(Manipulator):
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


class CompositeManipulator(Manipulator):
    def __init__(self, *args):
        super().__init__()
        self.rules = list(args)

    def apply(self, container):
        for rule in self.rules:
            rule.apply(container)

    def __add__(self, other):
        if isinstance(other, dict):
            manipulator = Append(**other)
        elif isinstance(other, Manipulator):
            manipulator = other
        else:
            raise TypeError('Only dict or Manipulator will be accepted')

        self.rules.append(manipulator)
        return self

    def __sub__(self, other):
        if isinstance(other, str):
            manipulator = Remove(other)
        elif isinstance(other, Iterable):
            manipulator = Remove(*other)
        elif isinstance(other, Manipulator):
            manipulator = other
        else:
            raise TypeError('Only str or an iterable of str will be accepted')

        self.rules.append(manipulator)
        return self

    def __or__(self, other):
        if isinstance(other, dict):
            manipulator = Update(**other)
        elif isinstance(other, Manipulator):
            manipulator = other
        else:
            raise TypeError('Only dict or Manipulator will be accepted')

        self.rules.append(manipulator)
        return self


class CompositeManipulatorInitializer(CompositeManipulator):
    def __add__(self, other):
        return CompositeManipulator() + other

    def __sub__(self, other):
        return CompositeManipulator() - other

    def __or__(self, other):
        return CompositeManipulator() | other

