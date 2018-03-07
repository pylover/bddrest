import unittest
import io

from bddrest.story import Story


class DocumentaryTestCase(unittest.TestCase):
    sample_yaml = '''
        base_call:
          as_: visitor
          response:
            headers:
            - 'Content-Type: application/json;charset=utf-8'
            json:
              foo: bar
            status: 200 OK
          title: Quickstart!
          url: /books/:id
          url_parameters:
            id: '1'
          verb: GET
        calls:
        - response:
            headers:
            - 'Content-Type: text/plain;charset=utf-8'
            status: 404 Not Found
          title: Trying invalid book id
          url_parameters:
            id: None
    '''
    def test_markdown(self):
        story = Story.loads(self.sample_yaml)
        outfile = io.BytesIO()
        markdown = story.document(outfile)
        self.assertEqual('''
        ''', markdown)


if __name__ == '__main__':
    unittest.main()

