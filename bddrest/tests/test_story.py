import unittest
import json

from bddrest import When, Then, Given, story, response, ReturnValueProxy, WsgiCall, CurrentStory


def wsgi_application(environ, start_response):
    start_response(200)
    return json.dumps(dict(
        secret='ABCDEF'
    ))


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
            self.assertIsInstance(response, ReturnValueProxy)

            # Then(
            #     response.status_code == 200,
            #     'secret' in response.body,
            #     response.body.secret == 'ABCDEF',
            #     'Bad Header' not in response.headers,
            #     response.headers.get('X-Pagination-Count') == '10',
            #     response.content_type == 'application/json'
            # )
            #
            # When(
            #     'Trying invalid code',
            #     form=dict(
            #         activationCode='badCode'
            #     )
            # )
            #
            # Then(400)

        # self.assertEqual('', story.dumps())


if __name__ == '__main__':
    unittest.main()
