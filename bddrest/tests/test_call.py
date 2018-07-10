import cgi
import functools
import json
import unittest

import pytest
from bddrest.exceptions import CallVerifyError
from bddrest.specification import Given, When


def wsgi_application(environ, start_response):
    form = cgi.FieldStorage(
        fp=environ['wsgi.input'],
        environ=environ,
        strict_parsing=False,
        keep_blank_values=True
    )

    start_response(
        '200 OK',
        [('Content-Type', 'application/json;charset=utf-8')]
    )
    result = dict(
        query=environ['QUERY_STRING'],
        url=environ['PATH_INFO']
    )
    if form and isinstance(form, dict):
        result.update(form)
    yield json.dumps(result).encode()


def test_call_constructor():
    call = Given('Testing Call contractor', url='/id: 1')
    assert call.url == '/:id'
    assert call.url_parameters == dict(id='1')

    call = Given(
        'Testing Call contractor',
        url='/id: 1/:name',
        url_parameters=dict(name='foo', id=2)
    )
    call.validate()
    assert call.url == '/:id/:name'
    assert call.url_parameters == dict(id='2', name='foo')
    call.conclude(wsgi_application)
    assert '/2/foo' == call.response.json['url']


def test_call_invoke():
    call = Given('Testing Call contractor', url='/id: 1')
    call.conclude(wsgi_application)
    assert call.response is not None


def test_call_response():
    call = Given('Testing Call contractor', url='/id: 1', query='a=1')
    call.conclude(wsgi_application)
    assert call.response is not None
    assert call.response.body is not None
    assert call.response.status == '200 OK'
    assert call.response.status_code == 200
    assert call.response.status_text == 'OK'
    assert call.response.encoding == 'utf-8'
    assert call.response.content_type == 'application/json'
    assert call.response.text is not None
    assert call.response.json == {'query': 'a=1', 'url': '/1'}
    assert call.response.headers == [
        ('Content-Type', 'application/json;charset=utf-8')
    ]


def test_call_to_dict():
    call = Given('Testing Call to_dict', url='/id: 1', query='a=1')
    call.conclude(wsgi_application)
    call_dict = call.to_dict()
    assert call_dict == dict(
        title='Testing Call to_dict',
        query=dict(a='1'),
        url='/:id',
        url_parameters={'id': '1'},
        verb='GET',
        response=dict(
            json={'query': 'a=1', 'url': '/1'},
            headers=['Content-Type: application/json;charset=utf-8'],
            status='200 OK',
        )
    )


def test_altered_call():
    call = Given('Testing When contractor', url='/id: 1', query=dict(a=1))
    altered_call = When(
        call,
        'Altering a call',
        query=dict(b=2)
    )
    altered_call.conclude(wsgi_application)
    assert altered_call.to_dict() == dict(
        title='Altering a call',
        query=dict(b=2),
        response=dict(
            status='200 OK',
            headers=['Content-Type: application/json;charset=utf-8'],
            json={'query': 'b=2', 'url': '/1'}
        )
    )


def test_call_verify():
    call = Given('Testing Given contractor', url='/id: 1', query=dict(a=1))
    call.conclude(wsgi_application)
    call.verify(wsgi_application)

    altered_call = When(
        call,
        'Altering a call',
        query=dict(b=2)
    )
    altered_call.conclude(wsgi_application)
    altered_call.verify(wsgi_application)

    altered_call.response.body = '{"a": 1}'
    with pytest.raises(CallVerifyError):
        altered_call.verify(wsgi_application)

    altered_call.response.status = '400 Bad Request'
    with pytest.raises(CallVerifyError):
        altered_call.verify(wsgi_application)


def test_querystring_parser():
    call = Given('Testing querystring parsing', url='/id: 1?a=1')
    assert '/:id' == call.url
    assert dict(a='1') == call.query

