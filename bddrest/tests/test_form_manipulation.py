import cgi
import json

from bddrest import Given, Append, when, response


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


def test_add_form_field():
    call = dict(
        title='test add form field',
        url='/apiv1/devices/name: SM-12345678/id: 1',
        verb='POST',
        form=dict(
            activationCode='746727',
            phone='+9897654321'
        ),
    )

    with Given(wsgi_application, **call):
        assert response.status == '200 OK'

        modified_call = when(
            'Adding another field',
            form=Append(email='user@example.com')
        )
        assert response.json == dict(
            activationCode='746727',
            phone='+9897654321',
            email='user@example.com'
        )
