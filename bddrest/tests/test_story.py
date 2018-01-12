import unittest
import json
import cgi

from bddrest import When, Then, Given, story, response, CurrentResponse, WsgiCall, CurrentStory, And


def wsgi_application(environ, start_response):
    form = cgi.FieldStorage(
        fp=environ['wsgi.input'],
        environ=environ,
        strict_parsing=False,
        keep_blank_values=True
    )

    try:
        code = int(form['activationCode'].value) ^ 1234
    except ValueError:
        start_response('400 Bad Request', [('Content-Type', 'text/plain;utf-8')])
        return

    start_response('200 OK', [
        ('Content-Type', 'application/json;encoding=utf-8'),
        ('X-Pagination-Count', '10')
    ])
    result = json.dumps(dict(
        secret='ABCDEF',
        code=code
    ))
    yield result.encode()


class StoryTestCase(unittest.TestCase):

    def test_given(self):
        call = WsgiCall(
            wsgi_application,
            title='Binding and registering the device after verifying the activation code',
            description='As a new visitor I have to bind my device with activation code and phone number',
            url='/apiv1/devices/name: SM-12345678',
            verb='BIND',
            as_='visitor',
            form=dict(
                activationCode='746727',
                phone='+9897654321'
            )
        )
        with Given(call):
            self.assertIsInstance(story, CurrentStory)
            self.assertIsInstance(response, CurrentResponse)

            Then(response.status == '200 OK')
            And(response.status_code == 200)
            And('secret' in response.json)
            And(response.json['secret'] == 'ABCDEF')
            And('Bad Header' not in response.headers)
            And(response.headers.get('X-Pagination-Count') == '10')
            And(response.content_type == 'application/json')
            And(self.assertDictEqual(response.json, dict(code=745525, secret='ABCDEF')))

            When(
                'Trying invalid code',
                form=dict(
                    activationCode='badCode'
                )
            )

            Then(response.status_code == 400)

        # self.assertEqual('', story.dumps())


if __name__ == '__main__':
    unittest.main()
