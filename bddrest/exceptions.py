
class BaseAssertionError(AssertionError):
    pass


class AttributeAssertionError(BaseAssertionError):
    def __init__(self, target, attribute):
        super().__init__(f'{type(target).__name__} has no attribute {attribute}')


class EqualityAssertionError(BaseAssertionError):
    def __init__(self, expected, actual):
        raise NotImplementedError()
