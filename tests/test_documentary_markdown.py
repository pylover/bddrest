import io

from bddrest import Story


def test_markdown():

    def get_field_info(call):
        return dict(), dict(
            f1=dict(required=True, not_none=True, type='str'),
        )

    story = Story.loads(provided_story)
    outfile = io.StringIO()
    story.document(onfile=lambda _: outfile, onstory=get_field_info)
    outputstring = outfile.getvalue()
    assert expected_markdown == outputstring


provided_story = '''
    base_call:
      as_: visitor
      title: Quickstart!
      description: Awesome API!
      path: /books/:id
      path_parameters:
        id: '1'
      query:
        a: 1
        b: '2'
      verb: PUT
      form:
        f1: abc
        f2: 123
      headers:
        - 'content-type: application/json;charset=utf-8'
      response:
        headers:
        - 'content-type: application/json;charset=utf-8'
        json:
          foo: bar
        status: 200 OK
    calls:
    - response:
        headers:
        - 'content-type: text/plain;charset=utf-8'
        status: 404 Not Found
      title: Trying invalid book id
      description: trying an invalid book id.
      path_parameters:
        id: None
      query:
        a: 2
        b: 4
      headers:
      - 'a: B'
      form:
        f1: cba
'''


expected_markdown = '''\
## Quickstart!

### PUT /books/:id

Awesome API!

### Path Parameters

Name | Example
--- | ---
id | 1

### Query Strings

Name | Example
--- | ---
a | 1
b | 2

### Form

Name | Required | Type | Example
--- | --- | --- | ---
f1 | Yes | str | abc
f2 | ? | ? | 123

### Request Headers

* content-type: application/json;charset=utf-8

### CURL

```bash
curl -X PUT -F "f1=abc" -F "f2=123" -H "content-type: application/json;charset=utf-8" -- "$URL/books/1?a=1&b=2"
```

### Response: 200 OK

#### Body

content-type: application/json

```json
{
  "foo": "bar"
}
```

---

## WHEN: Trying invalid book id

### PUT /books/:id

trying an invalid book id.

### Path Parameters

Name | Example
--- | ---
id | None

### Query Strings

Name | Example
--- | ---
a | 2
b | 4

### Form

Name | Required | Type | Example
--- | --- | --- | ---
f1 | Yes | str | cba

### Request Headers

* a: B

### CURL

```bash
curl -X PUT -F "f1=cba" -H "a: B" -- "$URL/books/None?a=2&b=4"
```

### Response: 404 Not Found

'''  # noqa
