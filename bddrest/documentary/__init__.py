from .formatters import *


class Documenter:
    def __init__(self, formatter_factory):
        self.formatter_factory = formatter_factory

    def document(self, story, outfile):
        formatter = self.formatter_factory(outfile)
        formatter.write_header1(story.title)

