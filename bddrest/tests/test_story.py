
import unittest

from bddrest import Story


class StoryTestCase(unittest.TestCase):
    def test_load_string(self):
        specification = '''
        description: As a new visitor I have to bind my device with activation code and phone number.
        given:
          url: /apiv1/devices/name: SM-12345678
          as: visitor
          verb: BIND
          form:
            activationCode: '746727'
            phone: '+9897654321'
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