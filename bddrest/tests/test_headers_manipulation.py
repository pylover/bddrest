import cgi
import json
import pytest

from bddrest import Given, Append, Remove, Update, when, response, status


def wsgi_application(environ, start_response):
    result = {}
    start_response('200 OK', [
        ('Content-Type', 'application/json;charset=utf-8'),
    ])

    for key in  [h for h in environ if h.startswith('HTTP')]:
        result[key[5:].lower()] = environ[key]

    yield json.dumps(result).encode()


def test_append_headers_field():
    with Given(
        wsgi_application,
        title='test add header field',
        url='/apiv1/devices/name: SM-12345678/id: 1',
        verb='POST',
        headers={'header1': '1'}
    ):
        assert status == '200 OK'
        assert response.json['header1'] == '1'

        # Using dictionary to manipulate lists, expecting error.
        with pytest.raises(ValueError):
            when('Adding new field to headers', headers=Append(header2='2'))

        when(
            'Adding new header: 2-tuple',
            headers=Append(('header2', '2'))
        )
        assert response.json['header1'] == '1'
        assert response.json['header2'] == '2'

        when(
            'Adding new header: single string',
            headers=Append('header3: 3')
        )
        assert response.json['header1'] == '1'
        assert response.json['header3'] == '3'
        assert 'header2' not in response.json



"""
def test_remove_headers_field():
     with Given(
        wsgi_application,
        title='test remove header fields',
        url='/apiv1/devices/name: SM-12345678/id: 1',
        verb='POST',
        form=dict(activationCode='746727'),
        headers={'token': '123456'}
     ):
        assert status == '200 OK'
        assert response.json['token'] == '123456'

        when('Token field has removed from headers', headers=Remove('token'))
        assert 'token' not in response.json

"""
