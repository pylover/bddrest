
import cgi
import json

from bddrest import Given, response, status, when


def wsgi_application(environ, start_response):
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

            result[k] = value.decode() if isinstance(value, bytes) else value

    start_response('200 OK', [
        ('Content-Type', 'application/json;charset=utf-8'),
    ])
    yield json.dumps(result).encode()


def test_none_parameters_within_form():
    form = dict(a=None)

    with Given(
        wsgi_application,
        title='test none parameters in a url-encoded form',
        verb='POST',
        form=form
    ):
        assert status == 200
        assert response.json['a'] == 'None'

    with Given(
        wsgi_application,
        title='test none parameters in a json form',
        verb='POST',
        json=form
    ):
        assert status == 200
        assert response.json['a'] is None

    with Given(
        wsgi_application,
        title='test none parameters in a multipart form',
        verb='POST',
        multipart=form
    ):
        assert status == 200
        assert response.json['a'] == 'None'


