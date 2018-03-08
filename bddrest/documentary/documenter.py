
class Documenter:
    def __init__(self, formatter_factory):
        self.formatter_factory = formatter_factory

    def write_response(self, formatter, response):
        formatter.write_header3(f'Response: {response.status}')

        if response.headers:
            formatter.write_header4('Headers')
            formatter.write_list(f'{k}: {v}' for k, v in response.headers)

        if response.body:
            formatter.write_header4('Body')
            mime = 'json' if 'json' in response.content_type else ''
            formatter.write_paragraph(f'```{mime}\n{response.text}\n```')


    def document(self, story, outfile):
        basecall = story.base_call
        formatter = self.formatter_factory(outfile)
        formatter.write_header2(basecall.title)
        formatter.write_header3(f'{basecall.verb} {basecall.url}')
        if basecall.description:
            formatter.write_paragraph(basecall.description)

        if basecall.query:
            formatter.write_header3('Query Strings')
            formatter.write_table(basecall.query.items(), headers=('Name', 'Example'))

        if basecall.form:
            formatter.write_header3('Form')
            formatter.write_table(basecall.form.items(), headers=('Name', 'Example'))

        if basecall.headers:
            formatter.write_header3('Request Headers')
            formatter.write_list(f'{k}: {v}' for k, v in basecall.headers)

        if basecall.response:
            self.write_response(formatter, basecall.response)

        for call in story.calls:
            formatter.write_header2(f'WHEN: {call.title}')

            if call.description:
                formatter.write_paragraph(call.description)

            if call.query and call.query != basecall.query:
                formatter.write_header3('Query Strings')
                formatter.write_table(call.query.items(), headers=('Name', 'Example'))

            if call.form and call.form != basecall.form:
                formatter.write_header3('Form')
                formatter.write_table(call.form.items(), headers=('Name', 'Example'))

            if call.headers and call.headers != basecall.headers:
                formatter.write_header3('Request Headers')
                formatter.write_list(f'{k}: {v}' for k, v in call.headers)

            if call.response:
                self.write_response(formatter, call.response)

