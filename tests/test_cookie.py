import json

from bddrest import Given, when, response, status, given


def wsgi_application(environ, start_response):
    cookies = environ['HTTP_COOKIE'].split(';')
    headers = [('Set-Cookie', c) for c in cookies]
    start_response('200 OK', headers)
    result = {}
    yield json.dumps(result).encode()


def test_append_headers_field():
    with Given(
        wsgi_application,
        title='test server cookies cookie',
        cookies={
            'foo': 'bar',
            'baz': 'qux',
        }
    ):
        assert status == '200 OK'
        assert response.cookies['foo'] == 'bar'
        assert response.cookies['baz'] == 'qux'

        when(cookies=given - 'foo')
        assert 'foo' not in response.cookies
        assert response.cookies['baz'] == 'qux'

        when(cookies=given + dict(thud='corge'))
        assert response.cookies['foo'] == 'bar'
        assert response.cookies['baz'] == 'qux'
        assert response.cookies['thud'] == 'corge'
