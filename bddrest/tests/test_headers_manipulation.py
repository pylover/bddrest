import cgi
import json
import pytest

from bddrest import Given, Append, Remove, Update, when, response, status


def wsgi_application(environ, start_response):
    result = {}
    start_response('200 OK', [
        ('Content-Type', 'application/json;charset=utf-8'),
    ])

    for key in [h for h in environ if h.startswith('HTTP')]:
        result[key[5:].lower()] = environ[key]

    yield json.dumps(result).encode()


def test_append_headers_field():
    with Given(
        wsgi_application,
        'test add header field',
        headers={'header1': '1'}
    ):
        assert status == '200 OK'
        assert response.json['header1'] == '1'

        # Using dictionary to manipulate lists, expecting error.
        with pytest.raises(ValueError):
            when('Abusing', headers=Append(header2='2'))

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


def test_remove_headers_field():
    with Given(
        wsgi_application,
        'test remove  header field',
        headers={'header1': '1'}
    ):
        assert status == '200 OK'
        assert response.json['header1'] == '1'

        when(
            'Removing an existing header: 2-tuple',
            headers=Remove(('header1', '1'))
        )
        assert 'header1' not in response.json

        when('Remove header by key', headers=Remove('header1'))

        # Remove an invalid header(Not exists)
        with pytest.raises(ValueError):
            when('Invalid  key', headers=Remove('invalid header'))
