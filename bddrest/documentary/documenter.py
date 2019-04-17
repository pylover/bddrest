import io

from .curl import CURL


class Documenter:
    def __init__(self, formatter_factory, fieldinfo=None):
        self.formatter_factory = formatter_factory
        self.fieldinfo = fieldinfo

    def write_response(self, formatter, response):
        formatter.write_header(f'Response: {response.status}', 3)
        ignore_headers = ['content-type']

        headers = {
            k: v for k, v in response.headers \
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
            formatter.write_paragraph(f'```{mime}\n{response.text}\n```')

    def write_curl(self, formatter, content):
        formatter.write_header('CURL', 3)
        formatter.write_paragraph(f'```bash\n{content}\n```')

    def write_call(self, basecall, call, formatter):

        formatter.write_header(f'{call.verb} {call.url}', 3)

        if call.description:
            formatter.write_paragraph(call.description)

        if call.url_parameters and (
                basecall is None or
                call.url_parameters != basecall.url_parameters
        ):
            formatter.write_header('Url Parameters', 3)
            formatter.write_table(
                call.url_parameters.items(),
                headers=('Name', 'Example')
            )

        if call.query and (
                basecall is None or
                call.query != basecall.query
        ):
            formatter.write_header('Query Strings', 3)
            formatter.write_table(
                call.query.items(),
                headers=('Name', 'Example')
            )

        if call.form and (
                basecall is None or
                call.form != basecall.form
        ):
            formatter.write_header('Form', 3)
            rows = []
            for k, v in call.form.items():
                info = self.fieldinfo(call.url, call.verb, k) \
                    if self.fieldinfo else None

                info = info or {}
                required = info.get('required')
                not_none = info.get('not_none')
                type_ = info.get('type')
                rows.append((
                    k,
                    '?' if required is None else required and 'Yes' or 'No',
                    '?' if not_none is None else not_none and 'No' or 'Yes',
                    '?' if type_ is None else type_,
                    v
                ))

            formatter.write_table(
                rows,
                headers=('Name', 'Required', 'Nullable', 'Type', 'Example')
            )

        if call.multipart and (
                basecall is None or
                call.multipart != basecall.multipart
        ):
            formatter.write_header('Multipart', 3)
            rows = []
            for k, v in call.multipart.items():
                info = self.fieldinfo(call.url, call.verb, k) \
                    if self.fieldinfo else None

                info = info or {}
                required = info.get('required')
                not_none = info.get('not_none')
                type_ = info.get('type')
                rows.append((
                    k,
                    '?' if required is None else required and 'Yes' or 'No',
                    '?' if not_none is None else not_none and 'No' or 'Yes',
                    '?' if type_ is None else type_,
                    v if not isinstance(v, io.BytesIO) else '<File>',
                ))

            formatter.write_table(
                rows,
                headers=('Name', 'Required', 'Nullable', 'Type', 'Example')
            )

        if call.json and not isinstance(call.json, list) and (
                basecall is None or
                call.json != basecall.json
        ):
            formatter.write_header('Form', 3)
            rows = []
            for k, v in call.json.items():
                info = self.fieldinfo(call.url, call.verb, k) \
                    if self.fieldinfo else None

                info = info or {}
                required = info.get('required')
                not_none = info.get('not_none')
                type_ = info.get('type')
                rows.append((
                    k,
                    '?' if required is None else required and 'Yes' or 'No',
                    '?' if not_none is None else not_none and 'No' or 'Yes',
                    '?' if type_ is None else type_,
                    v
                ))

            formatter.write_table(
                rows,
                headers=('Name', 'Required', 'Nullable', 'Type', 'Example')
            )

        if call.headers and (
                basecall is None or
                call.headers != basecall.headers
        ):
            formatter.write_header('Request Headers', 3)
            formatter.write_list(f'{k}: {v}' for k, v in call.headers)

        self.write_curl(formatter, CURL.from_call(call))

        if call.response:
            self.write_response(formatter, call.response)

    def document(self, story, outfile):
        basecall = story.base_call
        formatter = self.formatter_factory(outfile)
        formatter.write_header(basecall.title.capitalize(), 2)
        self.write_call(None, basecall, formatter)

        for call in story.calls:
            formatter.write_paragraph('---')
            formatter.write_header(f'WHEN: {call.title}', 2)
            self.write_call(basecall, call, formatter)

