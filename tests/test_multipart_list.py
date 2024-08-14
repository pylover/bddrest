import base64
import hashlib
import io
import json

from bddrest import Given, response, status

from . import multipart


def wsgi_application(environ, start_response):
    _, files = multipart.parse_form_data(
        environ,
        charset="utf8",
        strict=True
    )

    start_response('200 OK', [
        ('Content-Type', 'text/plain;charset=utf-8'),
    ])
    file1 = files['a'][0].file
    file2 = files['a'][1].file
    response = dict(
        file1=base64.encodebytes(hashlib.md5(file1.read()).digest()).decode(),
        file2=base64.encodebytes(hashlib.md5(file2.read()).digest()).decode()
    )
    yield json.dumps(response).encode()


BINARY_CONTENT1 = \
    b'{\xe2\xbd\x8a\x8eo\x19\x88\xbe\xf1+\xb6}\xccqoDz\xf3\xb7>\x8c\x83' \
    b'\x0f\xfe\xecj\xbcg\xbe0\x0f\xe25\x1d\x80\x1f\x023\x16\xe0\xf8\x0f' \
    b'\xc8\xca!\xe8\x01\n'


BINARY_CONTENT2 = \
    b'{\xe2\xbd\x8a\x8eo\x19\x88\xbe\xf1+\xb6}\xccqoDz\xf3\xb7>\x8c\x83' \
    b'\x0f\xfe\xecj\xbcg\xbe0\x0f\xe25\x1d\x80\x1f\x023\x16\xe0\xf8\x0f' \
    b'\xc8\xca!\xe8\x02\n'


BINARY_CONTENT_HASH1 = hashlib.md5(BINARY_CONTENT1).digest()
BINARY_CONTENT_HASH2 = hashlib.md5(BINARY_CONTENT2).digest()


def test_upload_list_of_file():
    call = dict(
        title='Uploading two files',
        verb='POST',
        multipart=dict(
            a=[
                io.BytesIO(BINARY_CONTENT1),
                io.BytesIO(BINARY_CONTENT2),
            ]
        )
    )

    with Given(wsgi_application, **call):
        assert status == '200 OK'
        assert base64.decodebytes(response.json['file1'].encode()) \
            == BINARY_CONTENT_HASH1

        assert base64.decodebytes(response.json['file2'].encode()) \
            == BINARY_CONTENT_HASH2
