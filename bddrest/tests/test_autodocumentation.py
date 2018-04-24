import tempfile
import unittest
from os import path
import io

from bddrest.authoring import given, then, response


def wsgi_application(environ, start_response):
    start_response('200 OK', [])
    yield b'Nothing'


class AutoDocumentationTestCase(unittest.TestCase):

    def test_autodoc_filename(self):
        filename = tempfile.mktemp()
        with given(
            wsgi_application,
            title='Testing auto documentation',
            url='/apiv1/devices/name: SM-12345678',
            autodoc=filename,
        ):
            then(response.status_code == 200)

        self.assertTrue(path.exists(filename))

    def test_autodoc_file_object(self):
        file = io.StringIO()
        with given(
            wsgi_application,
            title='Testing auto documentation',
            url='/apiv1/devices/name: SM-12345678',
            autodoc=file,
        ):
            then(response.status_code == 200)

        self.assertTrue(len(file.getvalue()) > 0)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()

