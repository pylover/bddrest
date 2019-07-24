from bddrest import Given, response, status, when


def wsgi_application(environ, start_response):
    fp = environ['wsgi.input']
    start_response('200 OK', [
        ('Content-Type', 'text/plain;charset=utf-8'),
    ])
    yield fp.read().decode('utf8')


def test_append_form_field():
    call = dict(
        title='test raw request body',
        verb='POST',
        body=b'abcd'
    )

    with Given(wsgi_application, **call):
        assert status == 200
        assert response.text == 'abcd'

        when('Another try!', body=b'1234')
        assert status == 200
        assert response.text == '1234'

