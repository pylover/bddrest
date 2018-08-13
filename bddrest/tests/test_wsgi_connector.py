import io
import os
import sys
import json
import cgi

from bddrest.response import Response
from bddrest.connectors import WSGIConnector


def test_wagi_streaming():
    def app(environ, start_response):
        write = start_response('200 Ok', [('Content-Type', 'aplication/json')])
        write(b'abc\n')
        return []

    connector = WSGIConnector(app)
    response = connector.request()
    assert isinstance(response, Response)
    assert response.text == 'abc\n'


def test_wsgi_yield():
    def app(environ, start_response):
        start_response('200 Ok', [('Content-Type', 'aplication/json')])
        yield 'abc\n'

    connector = WSGIConnector(app)
    response = connector.request()
    assert response.text == 'abc\n'


def test_wsgi_forms():
    def app(environ, start_response):
        if environ.get('CONTENT_TYPE', '').startswith('application/json'):
            result = json.loads(environ['wsgi.input'].read())
        else:
            form = cgi.FieldStorage(
                fp=environ['wsgi.input'],
                environ=environ,
                strict_parsing=False,
                keep_blank_values=True
            )
            result = {}
            for k in form.keys():
                v = form[k]
                value = v.value

                result[k] = \
                    value.decode() if isinstance(value, bytes) else value

        start_response('200 OK', [
            ('Content-Type', 'application/json;charset=utf-8'),
        ])
        yield json.dumps(result).encode()

    connector = WSGIConnector(app)

    # Simple string as request body with JSON content type
    response = connector.request(
        'POST',
        headers=[('Content-Type', 'application/json')],
        body='{"a": "b"}'
    )
    assert response.json.items() == dict(a='b').items()

    # JSON form
    response = connector.request(
        'POST',
        json=dict(a='b')
    )
    assert response.json.items() == dict(a='b').items()

    # url encoded:
    response = connector.request('POST', form=dict(a=1, b=2))
    assert response.json.items() == dict(a='1', b='2').items()

    # multipart
    form = {
        'a': 1,
        'b': io.StringIO('Hello')
    }
    response = connector.request('POST', multipart=form)
    assert response.json.items() == dict(a='1', b='Hello').items()


def test_query_string():
    def app(environ, start_response):
        query = environ['QUERY_STRING']
        start_response('200 OK', [
            ('Content-Type', 'text/plain'),
        ])
        yield query

    connector = WSGIConnector(app)

    response = connector.request(
        'POST',
        '/?a=b'
    )

    assert response.text == 'a=b'

