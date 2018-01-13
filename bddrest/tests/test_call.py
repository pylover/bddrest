import unittest
import cgi
import json
import functools

from bddrest import WsgiCall


def wsgi_application(environ, start_response):
    form = cgi.FieldStorage(
        fp=environ['wsgi.input'],
        environ=environ,
        strict_parsing=False,
        keep_blank_values=True
    )

    start_response('200 OK', [('Content-Type', 'application/json;charset=utf-8')])
    result = dict(query=environ['QUERY_STRING'])
    if form and isinstance(form, dict):
        result.update(form)
    yield json.dumps(result).encode()


Call = functools.partial(WsgiCall, wsgi_application)


class CallTestCase(unittest.TestCase):

    def test_call_constructor(self):
        call = Call('Testing Call contractor', url='/id: 1')
        self.assertEqual(call.url, '/:id')
        self.assertDictEqual(call.url_parameters, dict(id='1'))

        call = Call('Testing Call contractor', url='/id: 1/:name', url_parameters=dict(name='foo'))
        self.assertEqual(call.url, '/:id/:name')
        self.assertDictEqual(call.url_parameters, dict(id='1', name='foo'))

    def test_call_invoke(self):
        call = Call('Testing Call contractor', url='/id: 1')
        call.invoke()
        self.assertIsNotNone(call.response)

    def test_call_response(self):
        call = Call('Testing Call contractor', url='/id: 1', query='a=1')
        call.invoke()
        self.assertIsNotNone(call.response)
        self.assertIsNotNone(call.response.buffer)
        self.assertEqual(call.response.status, '200 OK')
        self.assertEqual(call.response.status_code, 200)
        self.assertEqual(call.response.status_text, 'OK')
        self.assertEqual(call.response.encoding, 'utf-8')
        self.assertEqual(call.response.content_type, 'application/json')
        self.assertEqual(call.response.text, '{"query": "a=1"}')
        self.assertDictEqual(call.response.json, {"query": "a=1"})
        self.assertListEqual(call.response.headers, [('Content-Type', 'application/json;charset=utf-8')])


if __name__ == '__main__':
    unittest.main()
