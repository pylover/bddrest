class ObjectProxy:
    """
    A simple object proxy to let deferred object's initialize later (for example: just after import):
    This class encapsulates some tricky codes to resolve the proxied object members using the
    `__getattribute__` and '__getattr__'. SO TAKE CARE about modifying the code, to prevent
    infinite loops and stack-overflow situations.

    Module: fancy_module

        deferred_object = None  # Will be initialized later.
        def init():
            global deferred_object
            deferred_object = AnyValue()
        proxy = ObjectProxy(lambda: deferred_object)

    In another module:

        from fancy_module import proxy, init
        def my_very_own_function():
            try:
                return proxy.any_attr_or_method()
            except: ObjectNotInitializedError:
                init()
                return my_very_own_function()

    """

    def __init__(self, resolver):
        object.__setattr__(self, '_resolver', resolver)

    @property
    def proxied_object(self):
        o = object.__getattribute__(self, '_resolver')()
        # if still is none, raise the exception
        if o is None:
            raise ValueError('Backend object is not initialized yet.')
        return o

    def __getattr__(self, key):
        return getattr(object.__getattribute__(self, 'proxied_object'), key)

    def __setattr__(self, key, value):
        setattr(object.__getattribute__(self, 'proxied_object'), key, value)

    def __eq__(self, other):
        return self.proxied_object.__eq__(other)

    def __gt__(self, other):
        return self.proxied_object.__gt__(other)

    def __ge__(self, other):
        return self.proxied_object.__ge__(other)

    def __lt__(self, other):
        return self.proxied_object.__lt__(other)

    def __le__(self, other):
        return self.proxied_object.__le__(other)

    def __str__(self):
        return self.proxied_object.__str__()

    def __repr__(self):
        return self.proxied_object.__repr__()

