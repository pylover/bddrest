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
          description: Awesome API!
          url: /books/:id
          url_parameters:
            id: '1'
          query:
            a: 1
            b: '2'
          verb: PUT
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
        story.document(outfile)
        outputstring = outfile.getvalue().decode()
        self.assertEqual(
            '## Quickstart!\n'
            '### PUT /books/:id\n'
            'Awesome API!\n'
            '### Query Strings\n'
            'Name | Example\n'
            '--- | ---\n'
            'a | 1\n'
            'b | 2\n'
            '',
            outputstring
        )
        print(outputstring)


if __name__ == '__main__':
    unittest.main()

