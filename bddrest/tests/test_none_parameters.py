
import cgi
import json

from bddrest import Given, response, status


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
    yield json.dumps({k: form[k].value for k in form.keys()}).encode()


def test_none_parameters_withen_form():
    call = dict(
        title='test none parameters in the form',
        verb='POST',
        content_type='application/json',
        form=dict(
            a=None,
        ),
    )

    with Given(wsgi_application, **call):
        assert status == 200
        assert response.json['a'] is None

