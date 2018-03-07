from .formatters import *


class Documenter:
    def __init__(self, formatter_factory):
        self.formatter_factory = formatter_factory

    def document(self, story, outfile):
        raise NotImplementedError()

