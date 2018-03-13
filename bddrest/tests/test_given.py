import unittest

from bddrest.specification import Given, When


class WhenTestCase(unittest.TestCase):

    def test_when_setters_deleters(self):
        basecall = Given(
            'Base call for testing When class',
            url='/apiv1/devices/id: 1',
        )

        when = When(
            basecall,
            title='Testing the When class',
            url='/apiv1/books/isbn: abc/pages/page: 3?highlight=false',
            verb='POST',
            form=dict(a='b'),
            headers=['A: B'],
            content_type='text/plain',
            as_='Admin',
            extra_environ=dict(A='B')
        )
        self.assertEqual('/apiv1/books/:isbn/pages/:page', when.url)
        self.assertDictEqual(dict(isbn='abc', page='3'), when.url_parameters)
        self.assertDictEqual(dict(highlight='false'), when.query)
        self.assertDictEqual(dict(a='b'), when.form)
        self.assertEqual('POST', when.verb)
        self.assertIn('A', when.headers)
        self.assertEqual('text/plain', when.content_type)
        self.assertEqual('Admin', when.as_)

        del when.url_parameters
        del when.verb
        del when.headers
        del when.query
        del when.content_type
        del when.as_
        del when.extra_environ
        del when.form

        self.assertDictEqual(dict(id='1'), when.url_parameters)
        self.assertEqual('GET', when.verb)
        self.assertIsNone(when.headers)
        self.assertIsNone(when.query)
        self.assertIsNone(when.form)
        self.assertIsNone(when.content_type)
        self.assertIsNone(when.as_)
        self.assertIsNone(when.extra_environ)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()


