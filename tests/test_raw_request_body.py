from bddrest import Given, response, status, when


def wsgi_application(environ, start_response):
    fp = environ['wsgi.input']
    start_response('200 OK', [
        ('Content-Type', 'text/plain;charset=utf-8'),
    ])
    clen = int(environ.get('CONTENT_LENGTH', 0))
    yield str(clen)
    if clen:
        yield ' '
        yield fp.read().decode('utf8')


def test_raw_requestbody():
    with Given(wsgi_application, verb='POST'):
        assert status == 200
        assert response.text == '0'

        when('Another try!', body=b'1234')
        assert status == 200
        assert response.text == '4 1234'

    with Given(wsgi_application, verb='POST', form='foobarbaz'):
        assert status == 200
        assert response.text == '10 foobarbaz='
