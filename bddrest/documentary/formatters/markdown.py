from .base import Formatter


class MarkdownFormatter(Formatter):
    def write_header1(self, text):
        self.writeline(f'# {text}')

    def write_header2(self, text):
        self.writeline(f'## {text}')

    def write_header3(self, text):
        self.writeline(f'### {text}')

    def write_header4(self, text):
        self.writeline(f'#### {text}')

    def write_header5(self, text):
        self.writeline(f'##### {text}')

    def write_header6(self, text):
        self.writeline(f'###### {text}')

