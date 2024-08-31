import json
from urllib.parse import parse_qs

from bddrest import Given, when, response


def wsgi_application(environ, start_response):
    fp = environ['wsgi.input']
    form = parse_qs(
        fp.read(int(environ.get('CONTENT_LENGTH'))).decode(),
        keep_blank_values=True,
        strict_parsing=False
    )

    try:
        code = int(form['activationCode'][0]) ^ 1234
    except ValueError:
        start_response(
            '400 Bad Request',
            [('Content-Type', 'text/plain;utf-8')]
        )
        return

    start_response('200 OK', [
        ('Content-Type', 'application/json;charset=utf-8'),
        ('X-Pagination-Count', '10')
    ])
    result = json.dumps(dict(
        code=code,
    ))
    yield result.encode()


def test_equality():

    call = dict(
        title='Binding and registering the device after verifying the '
              'activation code',
        description='As a new visitor I have to bind my device with '
                    'activation code and phone number',
        path='/apiv1/devices/name: SM-12345678',
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
        assert response == '{"code": 745525}'
        assert response == {
            'code': 745525,
        }

        when(
            'Trying invalid code',
            form=dict(
                activationCode='badCode'
            )
        )
        assert response.status == 400
