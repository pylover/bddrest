
class BaseAssertionError(AssertionError):
    pass


class AttributeAssertionError(BaseAssertionError):
    def __init__(self, object, attribute):
        raise NotImplementedError()


class EqualityAssertionError(BaseAssertionError):
    def __init__(self, expected, actual):
        raise NotImplementedError()
