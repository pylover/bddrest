import abc
import io
import json as libjson
from urllib.parse import urlencode

from .response import Response
from .helpers import encode_multipart_data


class WSGIResponse(Response):
    def write(self, data):
        if self.body is None:
            self.body = b''

        if isinstance(data, str):
            self.body += data.encode()
        else:
            self.body += data


class Connector(metaclass=abc.ABCMeta):
    def request(self, verb='GET', url='/', form=None, multipart=None,
                json=None, environ=None, headers=None, body=None, **kw):
        headers = headers or []

        if body is None:
            if multipart:
                content_type, body, content_length = \
                    encode_multipart_data(multipart)
                headers.append(('Content-Type', content_type))
                headers.append(('Content-Length', str(content_length)))

            elif json:
                body = libjson.dumps(json)
                headers.append(
                    ('Content-Type', 'application/json;charset:utf-8')
                )
                headers.append(('Content-Length', str(len(body))))

            elif isinstance(form, dict):
                body = urlencode(form)
                headers.append(
                    ('Content-Type', 'application/x-www-form-urlencoded')
                )

        if isinstance(body, str):
            body = body.encode()

        return self._send_request(verb, url, environ, headers, body)

    @abc.abstractmethod
    def _send_request(self, verb, url, environ, headers, body=None, **kw):
        pass


class WSGIConnector(Connector):
    def __init__(self, application, environ=None):
        self.application = application
        self.environ = environ

    def _prepare_environ(self, verb, url, headers, form=None,
                         extra_environ=None):
        if isinstance(form, io.BytesIO):
            input_file = form
        elif form:
            input_file = io.BytesIO(form)
            input_file.seek(0)
        else:
            input_file = io.BytesIO()

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

        if '?' in url:
            url, query = url.split('?', 1)
        else:
            query = ''
        environ['QUERY_STRING'] = query
        environ['PATH_INFO'] = url

        if extra_environ:
            environ.update(extra_environ)

        for k, v in headers:
            key = k.upper().replace('-', '_')
            if key not in ['CONTENT_TYPE', 'CONTENT_LENGTH']:
                key = 'HTTP_' + key
            environ[key] = v

        return environ

    def _send_request(self, verb, url, environ, headers, body=None, **kw):
        environ_ = self._prepare_environ(verb, url, headers, body, environ)
        response = None

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

