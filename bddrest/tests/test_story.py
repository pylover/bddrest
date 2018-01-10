import unittest

from bddrest import Story, given, Given, When, Then


class StoryTestCase(unittest.TestCase):
    def test_types(self):
        given_object = given(url='/apiv1/devices/')
        self.assertIsInstance(Given, given_object)

        then_object = given_object.then()
        self.assertIsInstance(Then, then_object)

        when_object = then_object.when('Action Title')
        self.assertIsInstance(When, when_object)

        story_object = then_object.story()
        self.assertIsInstance(Story, story_object)

    def test_given(self):
        story = given(
            title='Binding and registering the device after verifying the activation code',
            description='As a new visitor I have to bind my device with activation code and phone number',
            url='/apiv1/devices/name: SM-12345678',
            verb='BIND',
            as_='visitor',
            form=dict(
                activationCode='746727',
                phone='+9897654321'
            )
        )\
            .then(200)\
            .body_contains(dict(
                secret='ABCDEF'
            ))\
            .no_header('Bad Header')\
            .header('X-Pagination-Count', '10')\
            .content_type('application/json')\
            .when(
                'Trying invalid code',
                form=dict(
                    activationCode='badCode'
                ))\
            .then(400)\
            .story()

        self.assertEqual('', story.dumps())


if __name__ == '__main__':
    unittest.main()
