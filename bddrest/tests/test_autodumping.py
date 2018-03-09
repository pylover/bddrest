import unittest
import json
import cgi
import functools
import tempfile
from os import path

from bddrest.story import Story
from bddrest.specification import Call, When, Given
from bddrest.authoring import given, when, then, composer, response, and_
from bddrest.exceptions import InvalidUrlParametersError, CallVerifyError


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


if __name__ == '__main__':
    unittest.main()

