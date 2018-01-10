import unittest
import functools
import json

from bddrest import RestApiStory, When, Then, Story


def wsgi_application(environ, start_response):
    start_response(200)
    return json.dumps(dict(
        secret='ABCDEF'
    ))


Given = functools.partial(RestApiStory, wsgi_application)


class StoryTestCase(unittest.TestCase):

    def test_given(self):
        call = dict(
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
        with Given(**call) as story:
            self.assertIsInstance(Story, story)
            Then(200)\
                .body_contains(dict(
                    secret='ABCDEF'
                ))\
                .no_header('Bad Header')\
                .header('X-Pagination-Count', '10')\
                .content_type('application/json')

            When(
                'Trying invalid code',
                form=dict(
                    activationCode='badCode'
                )
            )

            Then(400)

        self.assertEqual('', story.dumps())


if __name__ == '__main__':
    unittest.main()
