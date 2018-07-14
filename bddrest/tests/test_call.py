import cgi
import functools
import json
import unittest

import pytest
from bddrest import CallVerifyError, FirstCall, AlteredCall


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
    call = FirstCall('Testing Call contractor', url='/id: 1')
    assert call.url == '/:id'
    assert call.url_parameters == dict(id='1')

    call = FirstCall(
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
    call = FirstCall('Testing Call contractor', url='/id: 1')
    call.conclude(wsgi_application)
    assert call.response is not None


def test_call_response():
    call = FirstCall('Testing Call contractor', url='/id: 1', query='a=1')
    call.conclude(wsgi_application)
    assert call.response is not None
    assert call.response.body is not None
    assert call.response.status == '200 OK'
    assert call.response.status == 200
    assert call.response.encoding == 'utf-8'
    assert call.response.content_type == 'application/json'
    assert call.response.text is not None
    assert call.response.json == {'query': 'a=1', 'url': '/1'}
    assert call.response.headers == [
        ('Content-Type', 'application/json;charset=utf-8')
    ]


def test_call_to_dict():
    call = FirstCall('Testing Call to_dict', url='/id: 1', query='a=1')
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
    call = FirstCall(
        'Testing AlteredCall contractor',
        url='/id: 1',
        query=dict(a=1)
    )

    altered_call = AlteredCall(
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


def test_alteredcall_setters_deleters():
    basecall = FirstCall(
        'Base call for testing When class',
        url='/apiv1/devices/id: 1',
    )

    when = AlteredCall(
        basecall,
        title='Testing the When class',
        url='/apiv1/books/isbn: abc/pages/page: 3?highlight=false',
        verb='POST',
        form=dict(a='b'),
        headers=['A: B'],
        content_type='text/plain',
        as_='Admin',
        extra_environ=dict(A='B')
    )
    assert '/apiv1/books/:isbn/pages/:page' == when.url
    assert dict(isbn='abc', page='3') == when.url_parameters
    assert dict(highlight='false') == when.query
    assert dict(a='b') == when.form
    assert 'POST' == when.verb
    assert 'A' in when.headers
    assert 'text/plain' == when.content_type
    assert 'Admin' == when.as_
    del when.url_parameters
    del when.verb
    del when.headers
    del when.query
    del when.content_type
    del when.as_
    del when.extra_environ
    del when.form

    assert dict(id='1') == when.url_parameters
    assert 'GET' == when.verb
    assert when.headers is None
    assert when.query is None
    assert when.form is None
    assert when.content_type is None
    assert when.as_ is None
    assert when.extra_environ is None


def test_call_verify():
    call = FirstCall(
        'Testing FirstCall contractor',
        url='/id: 1',
        query=dict(a=1)
    )

    call.conclude(wsgi_application)
    call.verify(wsgi_application)

    altered_call = AlteredCall(
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
    call = FirstCall('Testing querystring parsing', url='/id: 1?a=1')
    assert '/:id' == call.url
    assert dict(a='1') == call.query


def test_form_parser():
    pyload = dict(a=1, b=2)
    call = FirstCall('Testing form parsing', form=pyload)
    assert call.form == pyload

