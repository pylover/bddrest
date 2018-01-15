import unittest
import json
import cgi

from bddrest import When, Then, Given, story, response, CurrentResponse, Call, CurrentStory, And


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
        ('Content-Type', 'application/json;charset=utf-8'),
        ('X-Pagination-Count', '10')
    ])
    result = json.dumps(dict(
        secret='ABCDEF',
        code=code,
        query=environ['QUERY_STRING']
    ))
    yield result.encode()


class StoryTestCase(unittest.TestCase):

    def test_given_when_then(self):
        call = Call(
            wsgi_application,
            title='Binding and registering the device after verifying the activation code',
            description='As a new visitor I have to bind my device with activation code and phone number',
            url='/apiv1/devices/name: SM-12345678',
            verb='BIND',
            as_='visitor',
            query=dict(
                a=1,
                b=2
            ),
            form=dict(
                activationCode='746727',
                phone='+9897654321'
            )
        )
        with Given(call):
            self.assertIsInstance(story, CurrentStory)
            self.assertIsInstance(response, CurrentResponse)

            Then(
                response.status == '200 OK',
                response.status_code == 200
            )
            And('secret' in response.json)
            And(response.json['secret'] == 'ABCDEF')
            And('Bad Header' not in response.headers)
            # And(response.headers.get('X-Pagination-Count') == '10')
            And(response.content_type == 'application/json')
            And(self.assertDictEqual(response.json, dict(
                code=745525,
                secret='ABCDEF',
                query='a=1&b=2'
            )))

            When(
                'Trying invalid code',
                form=dict(
                    activationCode='badCode'
                )
            )

            Then(response.status_code == 400)

    # def test_to_dict(self):
    #     call = WsgiCall(
    #         wsgi_application,
    #         title='Binding',
    #         url='/apiv1/devices/name: SM-12345678',
    #         verb='BIND',
    #         as_='visitor',
    #         form=dict(
    #             activationCode='746727',
    #             phone='+9897654321'
    #         ),
    #         headers=[('X-H1', 'Header Value')]
    #     )
    #     with Given(call):
    #         self.assertIsInstance(story, CurrentStory)
    #         self.assertIsInstance(response, CurrentResponse)
    #         Then(response.status == '200 OK')
    #         When(
    #             'Trying invalid code',
    #             form=dict(
    #                 activationCode='badCode'
    #             )
    #         )
    #         Then(response.status_code == 400)
    #         story_dict = story.to_dict()
    #         self.maxDiff = None
    #         self.assertDictEqual(story_dict['given'], dict(
    #             title='Binding',
    #             url='/apiv1/devices/:name',
    #             verb='BIND',
    #             as_='visitor',
    #             url_parameters=dict(name='SM-12345678'),
    #             form=dict(
    #                 activationCode='746727',
    #                 phone='+9897654321'
    #             ),
    #             headers=['X-H1: Header Value'],
    #             response=dict(
    #                 status='200 OK',
    #                 headers=[
    #                     'Content-Type: application/json;charset=utf-8',
    #                     'X-Pagination-Count: 10'
    #                 ],
    #                 body='{"secret": "ABCDEF", "code": 745525, "query": ""}'
    #             )
    #         ))
    #         self.assertDictEqual(story_dict['calls'][0], dict(
    #             title='Trying invalid code',
    #             form=dict(
    #                 activationCode='badCode'
    #             )
    #         ))


if __name__ == '__main__':
    unittest.main()
