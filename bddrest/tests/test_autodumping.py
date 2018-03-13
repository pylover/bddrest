import tempfile
import unittest
from os import path

from bddrest.authoring import given, then, response


def wsgi_application(environ, start_response):
    start_response('200 OK', [])
    yield b'Nothing'


class StoryTestCase(unittest.TestCase):

    def test_autodump_composer(self):
        filename = tempfile.mktemp()
        with given(
            wsgi_application,
            title='Testing auto dump',
            url='/apiv1/devices/name: SM-12345678',
            autodump=filename,
        ):

            then(response.status == '200 OK')

        self.assertTrue(path.exists(filename))


if __name__ == '__main__':  # pragma: no cover
    unittest.main()

