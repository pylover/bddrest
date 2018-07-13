import tempfile
import unittest
from os import path
import io

from bddrest import  Given, response


def wsgi_application(environ, start_response):
    start_response('200 OK', [])
    yield b'Nothing'


def test_autodump_filename():
    filename = tempfile.mktemp()
    with Given(
        wsgi_application,
        title='Testing auto dump',
        url='/apiv1/devices/name: SM-12345678',
        autodump=filename,
    ):
        assert response.status == 200

    assert path.exists(filename)


def test_autodump_file_object():
    file = io.StringIO()
    with Given(
        wsgi_application,
        title='Testing auto dump',
        url='/apiv1/devices/name: SM-12345678',
        autodump=file,
    ):
        assert response.status  == 200

    assert len(file.getvalue()) > 0

