from bddcli import Given, when, stdout, status, stderr, Application


app = Application('bddrest', 'bddrest.cli:main')


def test_document_cli():
    with Given(app, ['document']):
        when(stdin=yamlstory)
        assert stderr == ''
        assert status == 0
        print(stdout)
        assert stdout == expected_markdown


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
  path: /books/:id
  path_parameters:
    id: '1'
  verb: GET
calls:
- response:
    headers:
    - 'Content-Type: text/plain;charset=utf-8'
    status: 404 Not Found
  title: Trying invalid book id
  path_parameters:
    id: None
'''

expected_markdown = '''\
## Posting a book

### GET /books/:id

As a member I have to POST a book to the library.

### Path Parameters

Name | Example
--- | ---
id | 1

### Query Strings

Name | Example
--- | ---
a | b

### Form

Name | Required | Type | Example
--- | --- | --- | ---
name | ? | ? | BDD Book

### CURL

```bash
curl -F "name=BDD Book" -- "$URL/books/1?a=b"
```

### Response: 200 OK

#### Body

Content-Type: application/json

```json
{
  "foo": "bar"
}
```

---

## WHEN: Trying invalid book id

### GET /books/:id

### Path Parameters

Name | Example
--- | ---
id | None

### CURL

```bash
curl -F "name=BDD Book" -- "$URL/books/None?a=b"
```

### Response: 404 Not Found

'''
