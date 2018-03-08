from abc import ABCMeta, abstractmethod


class Formatter(metaclass=ABCMeta):
    def __init__(self, outfile):
        self.file = outfile

    def write(self, text):
        self.file.write(text.encode())

    def writeline(self, text):
        self.write(f'{text}\n')

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

