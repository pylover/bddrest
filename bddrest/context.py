import threading


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


