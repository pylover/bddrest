import json

from bddrest.authoring import Given, when, response, status


def wsgi_application(environ, start_response):
    path = environ['PATH_INFO']
    if path.endswith('/None'):
        start_response(
            '404 Not Found',
            [('Content-Type', 'text/plain;charset=utf-8')]
        )
        yield b''
    else:
        start_response(
            '200 OK',
            [('Content-Type', 'application/json;charset=utf-8')]
        )
        result = json.dumps(dict(
            foo='bar'
        ))
        yield result.encode()


with Given(
        wsgi_application,
        title='Quickstart!',
        url='/books/id: 1',
        as_='visitor') as story:

    assert status == 200
    assert status == '200 OK'
    assert 'foo' in response.json
    assert response.json['foo'] == 'bar'

    when(
        'Trying invalid book id',
        url_parameters={'id': None}
    )

    assert response.status == 404
