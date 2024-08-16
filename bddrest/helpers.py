import base64
import io
import os
from mimetypes import guess_type
from urllib.parse import parse_qs, urlencode


def querystring_parse(query):
    if not query:
        return None

    if isinstance(query, str):
        query = parse_qs(
            query,
            keep_blank_values=True,
        )

    elif isinstance(query, dict):
        query = {
            k: v if isinstance(v, list) else [v] for k, v in query.items()
        }
    else:
        raise TypeError('Only dict and str is supported')

    return query


def querystring_encode(query):
    qs = []

    if query is None:
        return ''

    for key, value in query.items():
        if isinstance(value, list):
            for v in value:
                qs.append((key, v))
        else:
            qs.append((key, value))

    return urlencode(qs)


def encode_multipart_data(fields):
    boundary = ''.join(
        ['-----', base64.urlsafe_b64encode(os.urandom(27)).decode()]
    )
    crlf = b'\r\n'
    lines = []

    for key, value in fields.items():
        values = [value] if not isinstance(value, list) else value
        for value in values:
            if hasattr(value, 'read'):
                filename = value.name if hasattr(value, 'name') else key
                lines.append('--' + boundary)
                lines.append(
                    'Content-Disposition: form-data; name="%s"; '
                    'filename="%s"' % (key, filename)
                )
                lines.append(
                    'Content-Type: %s' %
                    (guess_type(filename)[0] or 'application/octet-stream')
                )
                lines.append('')
                lines.append(value.read())

            else:
                lines.append('--' + boundary)
                lines.append('Content-Disposition: form-data; name="%s"' % key)
                lines.append('')
                if not isinstance(value, str):
                    value = str(value)

                lines.append(value)

    lines.append('--' + boundary + '--')
    lines.append('')

    body = io.BytesIO()
    length = 0
    for line in lines:
        line = (line if isinstance(line, bytes) else line.encode()) + crlf
        length += len(line)
        body.write(line)
    body.seek(0)
    content_type = 'multipart/form-data; boundary=%s' % boundary
    return content_type, body, length
