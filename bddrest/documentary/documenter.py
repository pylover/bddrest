
class Documenter:
    def __init__(self, formatter_factory):
        self.formatter_factory = formatter_factory

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

