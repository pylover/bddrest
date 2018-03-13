import cgi
import functools
import json
import unittest

from bddrest.exceptions import CallVerifyError
from bddrest.specification import Given, When


def wsgi_application(environ, start_response):
    form = cgi.FieldStorage(
        fp=environ['wsgi.input'],
        environ=environ,
        strict_parsing=False,
        keep_blank_values=True
    )

    start_response('200 OK', [('Content-Type', 'application/json;charset=utf-8')])
    result = dict(
        query=environ['QUERY_STRING'],
        url=environ['PATH_INFO']
    )
    if form and isinstance(form, dict):
        result.update(form)
    yield json.dumps(result).encode()


class CallTestCase(unittest.TestCase):

    def test_call_constructor(self):
        call = Given('Testing Call contractor', url='/id: 1')
        self.assertEqual(call.url, '/:id')
        self.assertDictEqual(call.url_parameters, dict(id='1'))

        call = Given(
            'Testing Call contractor',
            url='/id: 1/:name',
            url_parameters=dict(name='foo', id=2)
        )
        call.validate()
        self.assertEqual(call.url, '/:id/:name')
        self.assertDictEqual(call.url_parameters, dict(id='2', name='foo'))
        call.conclude(wsgi_application)
        self.assertEqual('/2/foo', call.response.json['url'])

    def test_call_invoke(self):
        call = Given('Testing Call contractor', url='/id: 1')
        call.conclude(wsgi_application)
        self.assertIsNotNone(call.response)

    def test_call_response(self):
        call = Given('Testing Call contractor', url='/id: 1', query='a=1')
        call.conclude(wsgi_application)
        self.assertIsNotNone(call.response)
        self.assertIsNotNone(call.response.body)
        self.assertEqual(call.response.status, '200 OK')
        self.assertEqual(call.response.status_code, 200)
        self.assertEqual(call.response.status_text, 'OK')
        self.assertEqual(call.response.encoding, 'utf-8')
        self.assertEqual(call.response.content_type, 'application/json')
        self.assertIsNotNone(call.response.text)
        self.assertDictEqual(call.response.json, {'query': 'a=1', 'url': '/1'})
        self.assertListEqual(
            call.response.headers,
            [('Content-Type', 'application/json;charset=utf-8')]
        )

    def test_call_to_dict(self):
        call = Given('Testing Call to_dict', url='/id: 1', query='a=1')
        call.conclude(wsgi_application)
        call_dict = call.to_dict()
        self.assertDictEqual(call_dict, dict(
            title='Testing Call to_dict',
            query=dict(a='1'),
            url='/:id',
            url_parameters={'id': '1'},
            verb='GET',
            response=dict(
                json={'query': 'a=1', 'url': '/1'},
                headers=['Content-Type: application/json;charset=utf-8'],
                status='200 OK',
            )
        ))

    def test_altered_call(self):
        call = Given('Testing When contractor', url='/id: 1', query=dict(a=1))
        altered_call = When(
            call,
            'Altering a call',
            query=dict(b=2)
        )
        altered_call.conclude(wsgi_application)
        self.assertDictEqual(altered_call.to_dict(), dict(
            title='Altering a call',
            query=dict(b=2),
            response=dict(
                status='200 OK',
                headers=['Content-Type: application/json;charset=utf-8'],
                json={'query': 'b=2', 'url': '/1'}
            )
        ))

    def test_call_verify(self):
        call = Given('Testing Given contractor', url='/id: 1', query=dict(a=1))
        call.conclude(wsgi_application)
        call.verify(wsgi_application)

        altered_call = When(
            call,
            'Altering a call',
            query=dict(b=2)
        )
        altered_call.conclude(wsgi_application)
        altered_call.verify(wsgi_application)

        altered_call.response.body = '{"a": 1}'
        self.assertRaises(
            CallVerifyError,
            functools.partial(altered_call.verify, wsgi_application)
        )

        altered_call.response.status = '400 Bad Request'
        self.assertRaises(
            CallVerifyError,
            functools.partial(altered_call.verify, wsgi_application)
        )


    def test_querystring_parser(self):
        call = Given('Testing querystring parsing', url='/id: 1?a=1')
        self.assertEqual('/:id', call.url)
        self.assertDictEqual(dict(a='1'), call.query)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
