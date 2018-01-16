
class Assert:

    def get_full_qualified_name(self):
        attribute_tree = []
        current = self
        while True:
            if isinstance(self, AttributeAssert):
                attribute_tree.insert(0, current.attribute_name)

            elif isinstance(self, RootAssert):
                break

            current = current.resolve()

        return '.'.join(attribute_tree)

    def __getattr__(self, name):
        return AttributeAssert(self, name)

    def resolve(self):
        raise NotImplementedError()


class RootAssert(Assert):
    def __init__(self, resolve):
        self.resolve = resolve


class AttributeAssert(Assert):
    def __init__(self, target, attribute_name=None):
        self.target = target
        self.attribute_name = attribute_name

    def resolve(self):
        return getattr(self.target, self.attribute_name)


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
