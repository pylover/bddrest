import base64
import cgi
import hashlib
import io

from bddrest import Given, response, status, story


def wsgi_application(environ, start_response):
    form = cgi.FieldStorage(
        fp=environ['wsgi.input'],
        environ=environ,
        strict_parsing=False,
        keep_blank_values=True
    )

    start_response('200 OK', [
        ('Content-Type', 'text/plain;charset=utf-8'),
    ])
    binary_file = form['a'].file
    yield base64.encodebytes(hashlib.md5(binary_file.read()).digest()).decode()


BINARY_CONTENT = \
    b'{\xe2\xbd\x8a\x8eo\x19\x88\xbe\xf1+\xb6}\xccqoDz\xf3\xb7>\x8c\x83' \
    b'\x0f\xfe\xecj\xbcg\xbe0\x0f\xe25\x1d\x80\x1f\x023\x16\xe0\xf8\x0f' \
    b'\xc8\xca!\xe8\x01\n'

BINARY_CONTENT_HASH = hashlib.md5(BINARY_CONTENT).digest()


expected_markdown = '''\
## Uploading an image

### POST /

### Multipart

Name | Required | Nullable | Type | Example
--- | --- | --- | --- | ---
a | ? | ? | ? | <File>

### CURL

```bash
curl -X POST -F "a=@<path/to/file>" -- "$URL/?"
```

### Response: 200 OK

#### Body

Content-Type: text/plain

```
L5uEQbqDZrdzj5AX9wjtVA==\n
```

'''

def test_upload_binary_file():

    call = dict(
        title='Uploading an image',
        verb='POST',
        multipart=dict(a=io.BytesIO(BINARY_CONTENT))
    )

    with Given(wsgi_application, **call):
        assert status == '200 OK'
        assert base64.decodebytes(response.body) == BINARY_CONTENT_HASH

        story_dict = story.to_dict()
        assert 'multipart' in story_dict['base_call']

        outfile = io.StringIO()
        story.document(outfile)
        outputstring = outfile.getvalue()
        assert 'Multipart' in outputstring
        assert expected_markdown == outputstring

