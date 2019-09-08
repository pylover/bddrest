import base64
import io
import os
from mimetypes import guess_type
from urllib.parse import parse_qs


def normalize_query_string(query):
    if not query:
        return None
    return {
        k: v[0] if len(v) == 1 else v for k, v in parse_qs(query).items()
    } if isinstance(query, str) else query


def encode_multipart_data(fields):
    boundary = ''.join(
        ['-----', base64.urlsafe_b64encode(os.urandom(27)).decode()]
    )
    crlf = b'\r\n'
    lines = []

    for key, value in fields.items():
        values = [value] if not isinstance(value, list) else value
        for value in values:
            if not hasattr(value, 'read'):
                lines.append('--' + boundary)
                lines.append('Content-Disposition: form-data; name="%s"' % key)
                lines.append('')
                if not isinstance(value, str):
                    value = str(value)

                lines.append(value)

            else:
                filename = value.name if hasattr(value, 'name') else key
                lines.append('--' + boundary)
                lines.append(
                    'Content-Disposition: form-data; name="%s"; filename="%s"' %
                    (key, filename)
                )
                lines.append(
                    'Content-Type: %s' %
                    (guess_type(filename)[0] or 'application/octet-stream')
                )
                lines.append('')
                lines.append(value.read())

    lines.append('--' + boundary + '--')
    lines.append('')

    body = io.BytesIO()
    length = 0
    for l in lines:
        line = (l if isinstance(l, bytes) else l.encode()) + crlf
        length += len(line)
        body.write(line)
    body.seek(0)
    content_type = 'multipart/form-data; boundary=%s' % boundary
    return content_type, body, length

