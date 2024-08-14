import json

from . import multipart

from bddrest import Given, response, status


def wsgi_application(environ, start_response):
    if environ.get('CONTENT_TYPE', '').startswith('application/json'):
        result = json.loads(environ['wsgi.input'].read())
    else:
        form, _ = multipart.parse_form_data(
            environ,
            charset="utf8",
            strict=True
        )
        result = {}
        for k in form.keys():
            value = form[k]

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
