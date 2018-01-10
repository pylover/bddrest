import unittest

from bddrest import Story, given


class StoryTestCase(unittest.TestCase):
    def test_given(self):
given(
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
    .then(400)


        specification = '''
        .
        given:
        when:
          response:
            body:
              createdAt: '2017-12-29T21:30:57.443613Z'
              id: 1
              name: SM-12345678
              phone: '+9897654321'
              secret: 489357ABCDEF
              session: ''
              udid: gd63h3u73434
            headers:
            - 'Content-Type: application/json; charset=utf-8'
            status_code: 200
            status_text: OK
          title: Binding and registering the device after verifying the activation code
          url_parameters: null
        '''

        story = Story.loads(specification)
        self.assertDictEqual()


if __name__ == '__main__':
    unittest.main()
