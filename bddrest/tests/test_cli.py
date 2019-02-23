
from bddcli import Command, when, stdout, status, stderr, Application

from bddrest.tests.helpers import standard_files_mockup


app = Application('bddrest', 'bddrest.cli:Main')


def test_document_cli():
    with Command(
            app,
            'Pass document for generate markdown',
            stdin=yamlstory,
            positionals=['document']
    ):
        assert status == 0
        assert stderr == ''
        assert stdout == expected_markdown


def test_help():
    with Command(app, 'Without any pramater for getting help.'):
        assert status == 0
        assert stderr == ''
        assert stdout == expected_help


yamlstory = '''
base_call:
  as_: visitor
  description: As a member I have to POST a book to the library.
  form:
    name: BDD Book
  query:
    a: b
  response:
    headers:
    - 'Content-Type: application/json;charset=utf-8'
    json:
      foo: bar
    status: 200 OK
  title: Posting a book
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


expected_markdown = '''\
## Posting a book

### GET /books/:id

As a member I have to POST a book to the library.

### Url Parameters

Name | Example
--- | ---
id | 1

### Query Strings

Name | Example
--- | ---
a | b

### Form

Name | Required | Nullable | Type | Example
--- | --- | --- | --- | ---
name | ? | ? | ? | BDD Book

### CURL

```bash
curl -F "name=BDD Book" -- "$URL/books/1?a=b"
```

### Response: 200 OK

#### Body

Content-Type: application/json

```json
{"foo": "bar"}
```

---

## WHEN: Trying invalid book id

### GET /books/:id

### Url Parameters

Name | Example
--- | ---
id | None

### CURL

```bash
curl -F "name=BDD Book" -- "$URL/books/None?a=b"
```

### Response: 404 Not Found

'''


expected_help = '''\
usage: bddrest [-h] {document,completion} ...

bddrest

optional arguments:
  -h, --help            show this help message and exit

Sub commands:
  {document,completion}
    document            Generates REST API Documentation from standard input
                        to standard output.
    completion          Bash auto completion using argcomplete python package.
'''

