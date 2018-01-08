

class Backend:

    def __call__(self, verb, url, *, query=None, environ=None, description=None, form=None):
        raise NotImplementedError()


class WSGIBackend(Backend):
    pass
