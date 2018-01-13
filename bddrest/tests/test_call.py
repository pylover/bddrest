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

    start_response('200 OK', [('Content-Type', 'application/json;encoding=utf-8')])
    result = dict(query=environ['QUERY_STRING'])
    if form:
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
