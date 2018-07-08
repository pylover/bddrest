import tempfile
import unittest
from os import path
import io

from bddrest.authoring import given, response


def wsgi_application(environ, start_response):
    start_response('200 OK', [])
    yield b'Nothing'


def test_autodoc_filename():
    filename = tempfile.mktemp()
    with given(
        wsgi_application,
        title='Testing auto documentation',
        url='/apiv1/devices/name: SM-12345678',
        autodoc=filename,
    ):
        assert response.status_code == 200

    assert path.exists(filename)


def test_autodoc_file_object():
    file = io.StringIO()
    with given(
        wsgi_application,
        title='Testing auto documentation',
        url='/apiv1/devices/name: SM-12345678',
        autodoc=file,
    ):
        assert response.status_code == 200

    assert len(file.getvalue()) > 0

