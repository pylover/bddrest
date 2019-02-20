import abc
import io
import json as libjson
import socket
from urllib.parse import urlencode

import bddrest
from .helpers import encode_multipart_data
from .response import Response


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
                json=None, environ=None, headers=None, body=None,
                content_type=None, content_length=None, **kw):
        headers = headers or []

        if body is None:
            if multipart:
                content_type, body, content_length = \
                    encode_multipart_data(multipart)

            elif json:
                body = libjson.dumps(json)
                content_type = 'application/json;charset:utf-8'
                content_length = len(body)

            elif isinstance(form, dict):
                body = urlencode(form)
                content_length = len(body)
                content_type = 'application/x-www-form-urlencoded'
        else:
            content_length = len(body)

        if isinstance(body, str):
            body = body.encode()
            content_length = len(body)

        if content_type is not None:
            headers.append(('Content-Type', content_type))

        if content_length is not None:
            headers.append(('Content-Length', str(content_length)))

        return self._send_request(verb, url, environ, headers, body)

    @abc.abstractmethod
    def _send_request(self, verb, url, environ, headers, body=None, **kw):
        pass


class WSGIConnector(Connector):
    def __init__(self, application, environ=None):
        self.application = application
        self.environ = environ

    def _prepare_environ(self, verb, url, headers, payload=None,
                         extra_environ=None):
        if isinstance(payload, io.BytesIO):
            input_file = payload
        elif payload:
            input_file = io.BytesIO(payload)
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
        environ['SERVER_NAME'] = socket.gethostname()
        environ['HTTP_HOST'] = 'bddrest-interceptor'
        environ['HTTP_PORT'] = 80
        environ['SERVER_PROTOCOL'] = 'HTTP/1.1\r\n'
        environ['REMOTE_ADDR'] = '127.0.0.1'
        environ['HTTP_USER_AGENT'] = f'Python bddrest/{bddrest.__version__}'

        if '?' in url:
            url, query = url.split('?', 1)
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
                raise exc_info[1]

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

