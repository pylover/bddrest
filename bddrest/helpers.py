import threading
from urllib.parse import parse_qs


thread_local = threading.local()


class ContextIsNotInitializedError(Exception):
    pass


class ContextStack(list):

    def push(self, item):
        self.append(item)

    @property
    def hasitem(self):
        return self

    @property
    def current(self):
        if not self.hasitem:
            raise ContextIsNotInitializedError()
        return self[-1]


class Context:
    thread_local_key = 'bddrest_context_stack'

    @classmethod
    def __context_stack__(cls):
        if not hasattr(thread_local, cls.thread_local_key):
            setattr(thread_local, cls.thread_local_key, ContextStack())
        return getattr(thread_local, cls.thread_local_key)

    def __enter__(self):
        self.__context_stack__().push(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        stack = self.__context_stack__()
        if stack.hasitem:
            stack.pop()

    @classmethod
    def get_current(cls):
        return cls.__context_stack__().current


class ObjectProxy(object):
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


def normalize_query_string(query):
    if not query:
        return None
    return {
        k: v[0] if len(v) == 1 else v for k, v in parse_qs(query).items()
    } if isinstance(query, str) else query

