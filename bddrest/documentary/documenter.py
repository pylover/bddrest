import io

from .curl import CURL
from .formatters import create as createformatter


class Documenter:
    def __init__(self, onfile, format='markdown', onstory=None):
        self.format = format
        self.onfile = onfile
        self.onstory = onstory

    def write_response(self, formatter, response):
        formatter.write_header(f'Response: {response.status}', 3)
        ignore_headers = ['content-type']

        headers = {
            k: v for k, v in response.headers
            if k.lower() not in ignore_headers
        }
        if headers:
            formatter.write_header('Headers', 4)
            formatter.write_list(f'{k}: {v}' for k, v in headers.items())

        if response.status.code == 200 and response.body:
            formatter.write_header('Body', 4)
            formatter.write_paragraph(f'Content-Type: {response.content_type}')
            mime = ''
            if response.content_type and 'json' in response.content_type:
                mime = 'json'
            formatter.write_codeblock(mime, response.text)

    def write_curl(self, formatter, content):
        formatter.write_header('CURL', 3)
        formatter.write_codeblock('bash', content)

    def write_call(self, basecall, call, formatter):
        formatter.write_header(f'{call.verb} {call.path}', 3)

        if self.onstory:
            _, fieldsinfo = self.onstory(basecall)
        else:
            fieldsinfo = {}

        if call.description:
            formatter.write_paragraph(call.description)

        if call.path_parameters \
                and (basecall is None
                     or call.path_parameters != basecall.path_parameters):
            formatter.write_header('Path Parameters', 3)
            formatter.write_table(
                call.path_parameters.items(),
                headers=('Name', 'Example')
            )

        if call.query and (basecall is None or call.query != basecall.query):
            formatter.write_header('Query Strings', 3)

            rows = []
            for k, value in call.query.items():
                if isinstance(value, list):
                    for v in value:
                        rows.append((k, v))
                else:
                    rows.append((k, value))

            formatter.write_table(rows, headers=('Name', 'Example'))

        if call.form and (basecall is None or call.form != basecall.form):
            formatter.write_header('Form', 3)
            rows = []
            for k, value in call.form.items():
                info = fieldsinfo.get(k, {})
                if info is None:
                    info = {}

                for v in value:
                    needed = info.get('required')
                    type_ = info.get('type')
                    rows.append((
                        k,
                        '?' if needed is None else needed and 'Yes' or 'No',
                        '?' if type_ is None else type_,
                        v
                    ))

            formatter.write_table(
                rows,
                headers=('Name', 'Required', 'Type', 'Example')
            )

        if call.multipart \
                and (basecall is None or call.multipart != basecall.multipart):
            formatter.write_header('Multipart', 3)
            rows = []
            for k, v in call.multipart.items():
                info = fieldsinfo.get(k, {})
                if info is None:
                    info = {}

                required = info.get('required')
                type_ = info.get('type')
                rows.append((
                    k,
                    '?' if required is None else required and 'Yes' or 'No',
                    '?' if type_ is None else type_,
                    v if not isinstance(v, io.BytesIO) else '<File>',
                ))

            formatter.write_table(
                rows,
                headers=('Name', 'Required', 'Type', 'Example')
            )

        if call.json and not isinstance(call.json, list) \
                and (basecall is None or call.json != basecall.json):
            formatter.write_header('Form', 3)
            rows = []
            for k, v in call.json.items():
                info = fieldsinfo.get(k, {})
                required = info.get('required')
                notnone = info.get('notnone')
                type_ = info.get('type')
                rows.append((
                    k,
                    '?' if required is None else required and 'Yes' or 'No',
                    '?' if notnone is None else notnone and 'No' or 'Yes',
                    '?' if type_ is None else type_,
                    v
                ))

            formatter.write_table(
                rows,
                headers=('Name', 'Required', 'Nullable', 'Type', 'Example')
            )

        if call.headers \
                and (basecall is None or call.headers != basecall.headers):
            formatter.write_header('Request Headers', 3)
            formatter.write_list(f'{k}: {v}' for k, v in call.headers)

        self.write_curl(formatter, CURL.from_call(call))

        if call.response:
            self.write_response(formatter, call.response)

    def document(self, story):
        basecall = story.base_call
        outfile = self.onfile(story)
        formatter = createformatter(self.format, outfile)
        formatter.write_header(basecall.title.capitalize(), 2)
        self.write_call(None, basecall, formatter)

        for call in story.calls:
            if call.title is None:
                continue

            formatter.write_hr()
            formatter.write_header(f'WHEN: {call.title}', 2)
            self.write_call(basecall, call, formatter)
