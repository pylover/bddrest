import io

from bddrest import Given, response


def wsgi_application(environ, start_response):
    start_response('200 OK', [])
    yield b'Nothing'


def test_autodoc_file_object():
    file = io.StringIO()
    with Given(
        wsgi_application,
        title='Testing auto documentation',
        path='/apiv1/devices/name: SM-12345678',
        autodoc=dict(onfile=lambda _: file),
    ):
        assert response.status == 200

    assert len(file.getvalue()) > 0
