from .base import Formatter


class HTMLFormatter(Formatter):
    def _opentag(self, tag, end=''):
        self.writeline(f'<{tag}{end}>')

    def _closetag(self, tag):
        self.writeline(f'</{tag}>')

    def _tag(self, tag, text=None):
        if text is None:
            self._opentag(tag, end='/')
            return

        self._opentag(tag)
        self.writeline(text)
        self._closetag(tag)

    def write_header(self, text, level=1):
        self._tag(f'h{level}', text)

    def write_paragraph(self, text):
        self._tag('p', text)

    def write_table(self, array2d, headers=None):
        array2d = list(array2d) if not isinstance(array2d, list) else array2d

        self._opentag('table')

        # Header
        if headers:
            self._opentag('tr')
            for h in headers:
                self._tag('th', h)
            self._closetag('tr')

        # Body
        for r in array2d:
            self._opentag('tr')
            for c in r:
                self._tag('td', c)
            self._closetag('tr')

        self._closetag('table')

    def write_list(self, listkind):
        self._opentag('ul')
        for i in listkind:
            self._tag('li', i)
        self._closetag('ul')

    def write_codeblock(self, language, codeblock):
        self._opentag('pre')
        self._opentag('code')
        self.writeline(codeblock)
        self._closetag('code')
        self._closetag('pre')

    def write_hr(self):
        self._tag('hr')
