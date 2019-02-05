import unittest

from bddrest.cli import main
from bddrest.tests.helpers import standard_files_mockup


def test_document_cli():
    with standard_files_mockup(
            yamlstory, argv=['bddrest', 'document']) as (stdout, stderr):
        main()

    assert expected_markdown == stdout.getvalue().decode()


def test_help():
    with standard_files_mockup(yamlstory, argv=['bddrest']) \
            as (stdout, stderr):
        main()

    assert expected_help == stdout.getvalue().decode()


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
curl -X GET -F "name=BDD Book"  -- "$URL/books/1?a=b"
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
curl -X GET -F "name=BDD Book"  -- "$URL/books/None?a=b"
```

### Response: 404 Not Found

'''


expected_help = '''\
usage: bddrest [-h] {document} ...

bddrest command line interface.

optional arguments:
  -h, --help  show this help message and exit

Sub Commands:
  {document}
    document  Generates REST API Documentation from standard input to standard
              output.
'''
