import os

from os import path


class DocumentGenerator:

    def __init__(self, formatter_factory, output_directory):
        self.formatter_factory = formatter_factory
        self.output_directory = output_directory

    def generate(self, story):
        os.makedirs(path.dirname(self.output_directory), exist_ok=True)
        if not path.exists(f'{self.output_directory}{story.base_call.title}.md'):
            with open(f'{self.output_directory}{story.base_call.title}.md', mode='w') as output_file:
                formatter = self.formatter_factory(output_file)
                formatter.add_header_1(story.base_call.title)
                formatter.add_header_2(f'{story.base_call.verb} `{story.base_call.url}`')

                if story.base_call.form is not None:
                    for k,v in story.base_call.form.items():
                        pass


class Formatter:
    def __init__(self, output_file):
        self.stream = output_file

    def add_header_1(self, value):
        raise NotImplementedError()

    def add_header_2(self, value):
        raise NotImplementedError()

    def add_header_3(self, value):
        raise NotImplementedError()

    def add_header_4(self, value):
        raise NotImplementedError()

    def add_header_5(self, value):
        raise NotImplementedError()

    def add_header_6(self, value):
        raise NotImplementedError()

    def add_paragraph(self, value):
        raise NotImplementedError()

    def add_table(self):
        raise NotImplementedError()


class MarkdownFormatter(Formatter):

    def add_header_1(self, value):
        self.stream.write(f'# {value}\n')

    def add_header_2(self, value):
        self.stream.write(f'## {value}')

    def add_header_3(self, value):
        self.stream.write(f'### {value}')

    def add_header_4(self, value):
        self.stream.write(f'#### {value}')

    def add_header_5(self, value):
        self.stream.write(f'##### {value}')

    def add_header_6(self, value):
        self.stream.write(f'###### {value}')

    def add_paragraph(self, value):
        raise NotImplementedError()

    def add_table(self):
        raise NotImplementedError()

