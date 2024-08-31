import json
from urllib.parse import parse_qs

import pytest

from bddrest import CallVerifyError, FirstCall, AlteredCall


def wsgi_application(environ, start_response):
    fp = environ['wsgi.input']
    form = parse_qs(
        fp.read(int(environ.get('CONTENT_LENGTH', 0))).decode(),
        keep_blank_values=True,
        strict_parsing=False
    )

    start_response(
        '200 OK',
        [('Content-Type', 'application/json;charset=utf-8')]
    )
    result = dict(
        query=environ.get('QUERY_STRING'),
        path=environ['PATH_INFO']
    )
    if form and isinstance(form, dict):
        result.update(form)

    yield json.dumps(result).encode()


def test_call_constructor():
    call = FirstCall(path='/id: 1')
    assert call.path == '/:id'
    assert call.path_parameters == dict(id='1')

    call = FirstCall(
        path='/id: 1/:name',
        path_parameters=dict(name='foo', id=2)
    )
    call.validate()
    assert call.path == '/:id/:name'
    assert call.path_parameters == dict(id='2', name='foo')
    call.conclude(wsgi_application)
    assert '/2/foo' == call.response.json['path']


def test_call_invoke():
    call = FirstCall(path='/id: 1')
    call.conclude(wsgi_application)
    assert call.response is not None


def test_call_response():
    call = FirstCall(path='/id: 1', query='a=1')
    call.conclude(wsgi_application)
    assert call.response is not None
    assert call.response.body is not None
    assert call.response.status == '200 OK'
    assert call.response.status == 200
    assert call.response.encoding == 'utf-8'
    assert call.response.content_type == 'application/json'
    assert call.response.text is not None
    assert call.response.json == {'query': 'a=1', 'path': '/1'}
    assert call.response.headers == [
        ('Content-Type', 'application/json;charset=utf-8')
    ]


def test_call_to_dict():
    call = FirstCall(title='Testing Call to_dict', path='/id: 1', query='a=1')
    call.conclude(wsgi_application)
    call_dict = call.to_dict()
    assert call_dict == dict(
        title='Testing Call to_dict',
        query=dict(a=['1']),
        path='/:id',
        path_parameters={'id': '1'},
        verb='GET',
        response=dict(
            json={'query': 'a=1', 'path': '/1'},
            headers=['Content-Type: application/json;charset=utf-8'],
            status='200 OK',
        )
    )


def test_altered_call():
    call = FirstCall(
        title='Testing AlteredCall contractor',
        path='/id: 1',
        query=dict(a=1)
    )

    altered_call = AlteredCall(
        call,
        title='Altering a call',
        query=dict(b=2)
    )
    altered_call.conclude(wsgi_application)
    assert altered_call.to_dict() == dict(
        title='Altering a call',
        query=dict(b=[2]),
        response=dict(
            status='200 OK',
            headers=['Content-Type: application/json;charset=utf-8'],
            json={'query': 'b=2', 'path': '/1'}
        )
    )


def test_alteredcall_setters_deleters():
    basecall = FirstCall(
        path='/apiv1/devices/id: 1',
    )

    when = AlteredCall(
        basecall,
        title='Testing the When class',
        path='/apiv1/books/isbn: abc/pages/page: 3?highlight=false',
        verb='POST',
        form=dict(a='b'),
        headers=['A: B'],
        content_type='text/plain',
        as_='Admin',
        extra_environ=dict(A='B')
    )
    assert '/apiv1/books/:isbn/pages/:page' == when.path
    assert dict(isbn='abc', page='3') == when.path_parameters
    assert dict(highlight=['false']) == when.query
    assert dict(a=['b']) == when.form
    assert 'POST' == when.verb
    assert 'A' in when.headers
    assert 'text/plain' == when.content_type
    assert 'Admin' == when.as_
    del when.path_parameters
    del when.verb
    del when.headers
    del when.query
    del when.content_type
    del when.as_
    del when.extra_environ
    del when.form

    assert dict(id='1') == when.path_parameters
    assert 'GET' == when.verb
    assert when.headers is None
    assert when.query is None
    assert when.form is None
    assert when.content_type is None
    assert when.as_ is None
    assert when.extra_environ is None


def test_call_verify():
    call = FirstCall(
        path='/id: 1',
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
    call = FirstCall(path='/id: 1?a=1')
    assert '/:id' == call.path
    assert dict(a=['1']) == call.query

    call = FirstCall(path='/id: 1?a=1&a=2')
    assert dict(a=['1', '2']) == call.query


def test_form_parser():
    pyload = dict(a=1, b=2)
    call = FirstCall(form=pyload)
    assert call.form == dict(a=[1], b=[2])
