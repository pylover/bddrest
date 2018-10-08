
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

    def write_call(self, basecall, call, formatter):
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

                if info is None:
                    info = dict(nullable='?', required='?')

                rows.append((k, info['required'], info['nullable'], v))

            formatter.write_table(
                rows,
                headers=('Name', 'Required', 'Nullable', 'Example')
            )

        if call.headers and (
                basecall is None or
                call.headers != basecall.headers
        ):
            formatter.write_header('Request Headers', 3)
            formatter.write_list(f'{k}: {v}' for k, v in call.headers)

        if call.response:
            self.write_response(formatter, call.response)

    def document(self, story, outfile):
        basecall = story.base_call
        formatter = self.formatter_factory(outfile)
        formatter.write_header(basecall.title.capitalize(), 2)
        formatter.write_header(f'{basecall.verb} {basecall.url}', 3)
        self.write_call(None, basecall, formatter)

        for call in story.calls:
            formatter.write_paragraph('---')
            formatter.write_header(f'WHEN: {call.title}', 2)
            self.write_call(basecall, call, formatter)

