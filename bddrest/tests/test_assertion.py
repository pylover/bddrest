import cgi
import json

from bddrest import Given, when, response


def wsgi_application(environ, start_response):
    form = cgi.FieldStorage(
        fp=environ['wsgi.input'],
        environ=environ,
        strict_parsing=False,
        keep_blank_values=True
    )

    try:
        code = int(form['activationCode'].value) ^ 1234
    except ValueError:
        start_response('400 Bad Request', [('Content-Type', 'text/plain;utf-8')])
        return

    start_response('200 OK', [
        ('Content-Type', 'application/json;charset=utf-8'),
        ('X-Pagination-Count', '10')
    ])
    result = json.dumps(dict(
        secret='ABCDEF',
        code=code,
        query=environ['QUERY_STRING']
    ))
    yield result.encode()


def test_equality():

    call = dict(
        title=\
            'Binding and registering the device after verifying the '
            'activation code',
        description=\
            'As a new visitor I have to bind my device with activation '
            'code and phone number',
        url='/apiv1/devices/name: SM-12345678',
        verb='POST',
        as_='visitor',
        query=dict(
            a=1,
            b=2
        ),
        form=dict(
            activationCode='746727',
            phone='+9897654321'
        )
    )
    with Given(wsgi_application, **call):
        assert response.status == '200 OK'
        assert response.status == 200

        when(
            'Trying invalid code',
            form=dict(
                activationCode='badCode'
            )
        )
        assert response.status == 400

