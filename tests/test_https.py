from wsgiref.util import guess_scheme

from bddrest import Given, when, response, status


def wsgi_application(environ, start_response):
    scheme = guess_scheme(environ)

    start_response('200 OK', [
        ('Content-Type', 'text/plain'),
    ])
    return scheme, ', ', environ['wsgi.url_scheme']


def test_https():
    with Given(wsgi_application, https=True):
        assert status == 200
        assert response == 'https, https'

    with Given(wsgi_application):
        assert status == 200
        assert response == 'http, http'

        when(https=True)
        assert status == 200
        assert response == 'https, https'
