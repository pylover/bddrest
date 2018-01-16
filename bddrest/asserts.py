class AssertionFailed(AssertionError):
    def __init__(self, message):
        super().__init__(message)


class Assert:
    def __init__(self, target):
        self.target = target

    def get_full_qualified_name(self):
        return self.target.get_full_qualified_name()

    def __getattr__(self, name):
        return AttributeAssert(self, name)

    def resolve(self):
        return self.target


class RootAssert(Assert):
    def __init__(self, target, name=''):
        super().__init__(target)
        self.name = name

    def get_full_qualified_name(self):
        return self.name


class AttributeAssert(Assert):
    def __init__(self, target, attribute_name=None):
        super().__init__(target)
        self.attribute_name = attribute_name

    def resolve(self):
        try:
            return getattr(self.target.resolve(), self.attribute_name)
        except AttributeError:
            raise AssertionFailed(
                f'Assertion Failed:\n'
                f'Object: {self.target.get_full_qualified_name()} has no attribute {self.attribute_name}'
            )

    def get_full_qualified_name(self):
        result = super().get_full_qualified_name()
        return f'{result}.{self.attribute_name}'

    # @property
    # def new_expression(self):
    #     return functools.partial(ExpressionProxy, self)
    #
    # def __eq__(self, other):
    #     return self.new_expression('==', other)
    #
    # def __ne__(self, other):
    #     return self.new_expression('!=', other, negative=True)
#
#
# class ExpressionProxy(ObjectProxy):
#
#     def __init__(self, backend, operator, expected, negative=None):
#         super().__init__(backend)
#         self.operator = operator
#         self.expected = expected
#         self.negative = negative
#
#     def evaluate(self):
#         actual = super().evaluate()
#         ok = eval(f'{actual} {self.operator} {self.expected}')
#         if not ok:
#             expression = f'response.{self.get_full_qualified_name()} {self.operator} {self.expected}'
#             print(f'The expression: {expression} is failed.')
#             print(f'{"Not " if self.negative else ""}Expected: {self.expected}')
#             print(f'Actual: {actual}')
