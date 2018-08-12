import abc
import io
from urllib.parse import urlencode

from .specification import Response
from .helpers import encode_multipart_data


class WSGIResponse(Response):
    def __init__(self, status, headers):
        super().__init__(status, headers, body=b'')

    def write(self, data):
        if isinstance(data, str):
            self.body += data.encode()
        else:
            self.body += data


class Connector(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def request(self, verb='GET', url='/', **kw):
        pass


class WSGIConnector(Connector):
    def __init__(self, application, environ=None):
        self.application = application
        self.environ = environ

    def _prepare_environ(self, verb, headers, form=None, extra_environ=None):
        if isinstance(form, io.BytesIO):
            input_file = form
        elif form:
            input_file = io.BytesIO(form)
            input_file.seek(0)
        else:
            input_file = None
        error_file = io.StringIO()
        environ = self.environ.copy() if self.environ else {}
        environ['wsgi.input'] = input_file
        environ['wsgi.errors'] = error_file
        environ['wsgi.version'] = (1, 0)
        environ['wsgi.multithread'] = False
        environ['wsgi.multiprocess'] = False
        environ['wsgi.run_once'] = True
        environ['wsgi.url_scheme'] = 'http'
        environ['REQUEST_METHOD'] = verb

        if extra_environ:
            environ.update(extra_environ)

        for k, v in headers:
            key = k.upper().replace('-', '_')
            if key not in ['CONTENT_TYPE', 'CONTENT_LENGTH']:
                key = 'HTTP_' + key
            environ[key] = v

        return environ

    def request(self, verb='GET', url='/', environ=None, headers=None,
                form=None, multipart=None, **kw):
        response = None
        headers = headers or []

        if multipart:
            content_type, form, content_length = \
                encode_multipart_data(multipart)
            headers.append(('Content-Type', content_type))
            headers.append(('Content-Length', content_length))

        elif isinstance(form, dict):
            form = urlencode(form)
            headers.append(
                ('Content-Type', 'application/x-www-form-urlencoded')
            )

        if isinstance(form, str):
            form = form.encode()

        # Create the environ dicitonary
        environ_ = self._prepare_environ(verb, headers, form, environ)

        def start_response(status, headers, exc_info=None):
            nonlocal response
            if exc_info:
                raise (exc_info[0], exc_info[1], exc_info[2])

            response = WSGIResponse(status, headers)
            return response.write

        result = self.application(
            environ_,
            start_response
        )

        try:
            for i in result:
                response.write(i)
        finally:
            if hasattr(result, 'close'):
                result.close()

        return response


