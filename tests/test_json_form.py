import io
import json

from bddrest import Given, when, response, given, status, story


def wsgi_application(environ, start_response):
    form = json.load(environ['wsgi.input'])
    start_response('200 OK', [
        ('Content-Type', 'application/json;charset=utf-8'),
    ])
    yield json.dumps(form).encode()


def test_update_json_fields():
    call = dict(
        title='test remove form fields',
        url='/apiv1/devices/name: SM-12345678/id: 1',
        verb='POST',
        json=dict(
            a='1',
            b=2
        )
    )

    with Given(wsgi_application, **call):
        assert response.status == '200 OK'
        assert response.json == dict(a='1', b=2)

        when(
            'Adding new field',
            json=given + dict(c=3)
        )
        assert response.json == dict(a='1', b=2, c=3)

        when(
            'Updating a field with None',
            json=given | dict(b=None)
        )
        assert response.json == dict(a='1', b=None)

        when(
            'Removing a field',
            json=given - 'a'
        )
        assert response.json == dict(b=2)


expected_markdown = '''\
## Testing auto documentation with json request

### POST /

### Form

Name | Required | Nullable | Type | Example
--- | --- | --- | --- | ---
a | ? | ? | ? | 1
b | ? | ? | ? | None
c | ? | ? | ? | False

### CURL

```bash
curl -X POST --data '{"a": 1, "b": null, "c": false}' -- "$URL/?"
```

### Response: 200 OK

#### Body

Content-Type: application/json

```json
{"a": 1, "b": null, "c": false}
```

'''


def test_autodocument_json():
    call = dict(
        title='Testing auto documentation with json request',
        verb='POST',
        json=dict(
            a=1,
            b=None,
            c=False,
        )
    )

    with Given(wsgi_application, **call):
        assert status == '200 OK'

        story_dict = story.to_dict()
        assert 'json' in story_dict['base_call']

        outfile = io.StringIO()
        story.document(outfile)
        outputstring = outfile.getvalue()
        assert 'Form' in outputstring
        assert expected_markdown == outputstring

