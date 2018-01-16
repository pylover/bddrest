import functools

class Body:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class Response:

    def __init__(self, status, **body):
        self.status = status
        self.body = Body(**body)


def then(*criteria):
    for criterion in criteria:
        criterion.evaluate()


class ObjectProxy:

    def __init__(self, backend, name=None):
        self._backend = backend
        self.name = name

    def __getattr__(self, name):
        return ObjectProxy(self, name)

    @property
    def __backend__(self):
        return self._backend

    def evaluate(self):
        backend_value = self.__backend__.evaluate() if isinstance(self.__backend__, ObjectProxy) else self.__backend__
        if self.name is None:
            return backend_value
        else:
            return getattr(backend_value, self.name)

    def get_full_qualified_name(self):
        attribute_tree = []
        o = self
        while True:
            if getattr(o, '__backend__', None) is None:
                # Is a root object
                break
            if o.name is not None:
                attribute_tree.insert(0, o.name)
            o = o.__backend__

        return '.'.join(attribute_tree)

    @property
    def new_expression(self):
        return functools.partial(ExpressionProxy, self)

    def __eq__(self, other):
        return self.new_expression('==', other)

    def __ne__(self, other):
        return self.new_expression('!=', other, negative=True)


class ExpressionProxy(ObjectProxy):

    def __init__(self, backend, operator, expected, negative=None):
        super().__init__(backend)
        self.operator = operator
        self.expected = expected
        self.negative = negative

    def evaluate(self):
        actual = super().evaluate()
        ok = eval(f'{actual} {self.operator} {self.expected}')
        if not ok:
            expression = f'response.{self.get_full_qualified_name()} {self.operator} {self.expected}'
            print(f'The expression: {expression} is failed.')
            print(f'{"Not " if self.negative else ""}Expected: {self.expected}')
            print(f'Actual: {actual}')


if __name__ == '__main__':
    r = Response(200, a=1, b=Body(c=3))
    response = ObjectProxy(r)
    # print(response.body.b.c.evaluate())
    # print(response.body.b.c.get_full_qualified_name())

    then(response.status == 201)
    then(response.status != 200)

    # print(eval(f'r.{response.body.b.c.get_full_qualified_name()}'))
    # then(response_proxy.body.a == 2)
