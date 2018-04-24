
class Documenter:
    def __init__(self, formatter_factory):
        self.formatter_factory = formatter_factory

    def write_response(self, formatter, response):
        formatter.write_header(f'Response: {response.status}', 3)

        if response.headers:
            formatter.write_header('Headers', 4)
            formatter.write_list(f'{k}: {v}' for k, v in response.headers)

        if response.body:
            formatter.write_header('Body', 4)
            mime = ''
            if response.content_type and 'json' in response.content_type:
                mime = 'json'
            formatter.write_paragraph(f'```{mime}\n{response.text}\n```')

    def document(self, story, outfile):
        basecall = story.base_call
        formatter = self.formatter_factory(outfile)
        formatter.write_header(basecall.title, 2)
        formatter.write_header(f'{basecall.verb} {basecall.url}', 3)
        if basecall.description:
            formatter.write_paragraph(basecall.description)

        if basecall.url_parameters:
            formatter.write_header('Url Parameters', 3)
            formatter.write_table(basecall.url_parameters.items(), headers=('Name', 'Example'))

        if basecall.query:
            formatter.write_header('Query Strings', 3)
            formatter.write_table(basecall.query.items(), headers=('Name', 'Example'))

        if basecall.form:
            formatter.write_header('Form', 3)
            formatter.write_table(basecall.form.items(), headers=('Name', 'Example'))

        if basecall.headers:
            formatter.write_header('Request Headers', 3)
            formatter.write_list(f'{k}: {v}' for k, v in basecall.headers)

        if basecall.response:
            self.write_response(formatter, basecall.response)

        for call in story.calls:
            formatter.write_header(f'WHEN: {call.title}', 2)

            if call.description:
                formatter.write_paragraph(call.description)

            if call.url_parameters and call.url_parameters != basecall.url_parameters:
                formatter.write_header('Url Parameters', 3)
                formatter.write_table(call.url_parameters.items(), headers=('Name', 'Example'))

            if call.query and call.query != basecall.query:
                formatter.write_header('Query Strings', 3)
                formatter.write_table(call.query.items(), headers=('Name', 'Example'))

            if call.form and call.form != basecall.form:
                formatter.write_header('Form', 3)
                formatter.write_table(call.form.items(), headers=('Name', 'Example'))

            if call.headers and call.headers != basecall.headers:
                formatter.write_header('Request Headers', 3)
                formatter.write_list(f'{k}: {v}' for k, v in call.headers)

            if call.response:
                self.write_response(formatter, call.response)

