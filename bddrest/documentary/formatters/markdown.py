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

    def write_paragraph(self, text):
        self.writeline(text)

    def _write_table_row(self, row):
        self.writeline(' | '.join(str(i) for i in row))

    def write_table(self, array2d, headers=None):
        if not isinstance(array2d, list):
            array2d = list(array2d)

        columns = len(array2d[0])
        if headers:
            self._write_table_row(headers)
        self.writeline(' | '.join(['---'] * columns))
        for row in array2d:
            self._write_table_row(row)

    def write_list(self, listkind):
        self.writeline()
        for l in listkind:
            self.writeline(f'* {l}')
        self.writeline()

