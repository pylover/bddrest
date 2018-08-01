import cgi
import json
import pytest

from bddrest import Given, Append, Remove, Update, when, response, status


def wsgi_application(environ, start_response):
    form = cgi.FieldStorage(
        fp=environ['wsgi.input'],
        environ=environ,
        strict_parsing=False,
        keep_blank_values=True
    )

    start_response('200 OK', [
        ('Content-Type', 'application/json;charset=utf-8'),
    ])

    result = {k: form[k].value for k in form.keys()}
    for key in  [h for h in environ if h.startswith('HTTP')]:
        result[key[5:].lower()] = environ[key]

    yield json.dumps(result).encode()


def test_append_headers_field():
    with Given(
        wsgi_application,
        title='test add header field',
        url='/apiv1/devices/name: SM-12345678/id: 1',
        verb='POST',
        form=dict(activationCode='746727'),
        headers={'token': '123456'}
    ):
        assert status == '200 OK'
        assert response.json['token'] == '123456'

        when('Adding new field to headers', headers=Append(new_token='654321'))
        assert response.json['new_token'] == '654321'

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

def test_update_headers_field():
    with Given(
        wsgi_application,
        title='test update header fields',
        url='/apiv1/devices/name: SM-12345678/id: 1',
        verb='POST',
        form=dict(activationCode='746727'),
        headers={'token': '123456'}
    ):
        assert status == '200 OK'
        assert response.json['token'] == '123456'

        when(
            'Token has been updated in heardes fields',
            headers=Update(token='654321')
        )
        assert response.json['token'] == '654321'

