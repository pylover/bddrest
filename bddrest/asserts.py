class AssertionFailed(AssertionError):
    def __init__(self, message):
        super().__init__(message)


class Assert:
    def __init__(self, target):
        self.target = target

    def __str__(self):
        return str(self.target)

    def resolve(self):
        return self.target

    def __getattr__(self, name):
        return AssertAttribute(self, name)

    def __getitem__(self, item):
        return AssertGetItem(self, item)

    def __eq__(self, other):
        return AssertComparison(self, '==', other)

    def __ne__(self, other):
        return AssertComparison(self, '!=', other, negative=True)

    def __gt__(self, other):
        return AssertComparison(self, '>', other)

    def __ge__(self, other):
        return AssertComparison(self, '>=', other)

    def __lt__(self, other):
        return AssertComparison(self, '<', other)

    def __le__(self, other):
        return AssertComparison(self, '<=', other)

    def __call__(self, *args, **kwargs):
        return AssertCall(self, args=args, kwargs=kwargs)


class AssertRoot(Assert):
    def __init__(self, target, name='target'):
        super().__init__(target)
        self.name = name

    def __str__(self):
        return self.name


class AssertAttribute(Assert):
    def __init__(self, target, attribute_name=None):
        super().__init__(target)
        self.attribute_name = attribute_name

    def resolve(self):
        try:
            return getattr(self.target.resolve(), self.attribute_name)
        except AttributeError:
            raise AssertionFailed(
                f'\nAssertion Failed:\n'
                f'Object: {self.target} has no attribute {self.attribute_name}'
            )

    def __str__(self):
        parent = super().__str__()
        return f'{parent}.{self.attribute_name}'


class AssertGetItem(Assert):
    def __init__(self, target, key=None):
        super().__init__(target)
        self.key = key

    def resolve(self):
        try:
            return self.target.resolve()[self.key]
        except (KeyError, IndexError):
            raise AssertionFailed(
                f'\nAssertion Failed:\n'
                f'Object: {self.target} has no item {self.key}'
            )

    def __str__(self):
        parent = super().__str__()
        if isinstance(self.key, slice):
            key = f'{self.key.start or ""}:{self.key.stop or ""}'
            if self.key.step:
                key += f':{self.key.step}'
        elif isinstance(self.key, str):
            key = f'\'{self.key}\''
        else:
            key = self.key
        return f'{parent}[{key}]'


class AssertComparison(Assert):
    def __init__(self, target, operator, expected, negative=False):
            super().__init__(target)
            self.operator = operator
            self.expected = expected
            self.negative = negative

    def resolve(self):
        actual = self.target.resolve()
        ok = eval(f'{actual} {self.operator} {self.expected}')
        if not ok:
            message = \
                f'\nThe expression:\n\n\t{self}\n\nhas been failed.\n'
            if self.operator in ('==', '!='):
                message += \
                    f'{"Not " if self.negative else ""}Expected: {self.expected}\nActual: {actual}'
            raise AssertionFailed(message)
        return ok

    def __str__(self):
        return f'{self.target} {self.operator} {self.expected}'


class AssertCall(Assert):
    def __init__(self, target, args=tuple(), kwargs={}):
            super().__init__(target)
            self.args = args
            self.kwargs = kwargs

    def resolve(self):
        actual = self.target.resolve()
        return actual(*self.args, **self.kwargs)

    def __str__(self):
        signature = ''

        def normalize(x):
            return f'\'{x}\'' if isinstance(x, str) else x

        if self.args:
            signature += ', '.join(normalize(a) for a in self.args)
        if self.kwargs:
            signature += ', ' if signature else ''
            signature += ', '.join(f'{k}={normalize(v)}' for k, v in self.kwargs.items())

        return f'{self.target}({signature})'


__all__ = [
    'AssertionFailed',
    'Assert',
    'AssertRoot',
    'AssertAttribute',
    'AssertGetItem',
    'AssertComparison',
    'AssertCall'
]
