from abc import ABCMeta, abstractmethod


class Formatter(metaclass=ABCMeta):
    def __init__(self, outfile):
        self.file = outfile

    def write(self, text):
        self.file.write(text)

    @abstractmethod
    def writeline(self, text=''):  # pragma: no cover
        pass

    @abstractmethod
    def write_header(self, text, level=1):  # pragma: no cover
        pass

    @abstractmethod
    def write_paragraph(self, text):  # pragma: no cover
        pass

    @abstractmethod
    def write_table(self, array2d, headers=None):  # pragma: no cover
        pass

    @abstractmethod
    def write_list(self, listkind):  # pragma: no cover
        pass

