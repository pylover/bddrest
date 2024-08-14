from bddrest import Given, when, response


def wsgi_application(environ, start_response):
    resp = environ.get('QUERY_STRING')
    start_response('200 OK', [
        ('Content-Type', 'text/plain;charset=utf-8'),
        ('Content-Length', str(0 if resp is None else len(resp))),
    ])

    if resp is not None:
        yield resp


def test_querystring():
    with Given(wsgi_application, query=dict(foo='')):
        assert response.status == 200
        assert response.text == 'foo='

        when(query='foo=bar')
        assert response.status == 200
        assert response.text == 'foo=bar'

        when(query='foo=')
        assert response.status == 200
        assert response.text == ''

        when(url='/?foo=')
        assert response.status == 200
        assert response.text == 'foo='

        when(query=dict(foo=''))
        assert response.status == 200
        assert response.text == 'foo='
