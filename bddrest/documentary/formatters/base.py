from abc import ABCMeta, abstractmethod


class Formatter(metaclass=ABCMeta):
    def __init__(self, outfile, cr='\n'):
        self.file = outfile
        self.cr = cr

    def write(self, text):
        self.file.write(text)

    def writeline(self, text=''):
        self.write(f'{text}{self.cr}')

    @abstractmethod
    def write_header(self, text, level=1):  # pragma: no cover
        raise NotImplementedError()

    @abstractmethod
    def write_paragraph(self, text):  # pragma: no cover
        raise NotImplementedError()

    @abstractmethod
    def write_table(self, array2d, headers=None):  # pragma: no cover
        raise NotImplementedError()

    @abstractmethod
    def write_list(self, items):  # pragma: no cover
        raise NotImplementedError()

    @abstractmethod
    def write_codeblock(self, language, codeblock):  # pragma: no cover
        raise NotImplementedError()

    @abstractmethod
    def write_hr(self):  # pragma: no cover
        raise NotImplementedError()
