from abc import ABCMeta, abstractmethod


class Formatter(metaclass=ABCMeta):
    def __init__(self, outfile):
        self.file = outfile

    def write(self, text):
        if not hasattr(self.file, 'encoding') or self.file.encoding.lower() != 'utf-8':
            text = text.encode()

        self.file.write(text)

    @abstractmethod
    def writeline(self, text=''):
        pass

    @abstractmethod
    def write_header1(self, text):
        pass

    @abstractmethod
    def write_header2(self, text):
        pass

    @abstractmethod
    def write_header3(self, text):
        pass

    @abstractmethod
    def write_header4(self, text):
        pass

    @abstractmethod
    def write_header5(self, text):
        pass

    @abstractmethod
    def write_header6(self, text):
        pass

    @abstractmethod
    def write_paragraph(self, text):
        pass

    @abstractmethod
    def write_table(self, array2d, headers=None):
        pass

    @abstractmethod
    def write_list(self, listkind):
        pass

