from bddrest import Given, when, response


def wsgi_application(environ, start_response):
    resp = environ.get('QUERY_STRING')
    start_response('200 OK', [
        ('Content-Type', 'text/plain;charset=utf-8'),
        ('Content-Length', str(0 if resp is None else len(resp))),
    ])

    if resp is not None:
        yield resp


def test_rawurl():
    with Given(wsgi_application, rawurl='/?foo'):
        assert response.status == 200
        assert response.text == 'foo'

        when(rawurl='/?foo&bar&baz')
        assert response.status == 200
        assert response.text == 'foo&bar&baz'
