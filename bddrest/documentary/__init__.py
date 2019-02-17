import sys

from easycli import SubCommand, Argument

from .formatters import *
from .documenter import Documenter

class DocumentaryLauncher(SubCommand):
    __command__ = 'document'
    __help__ = 'Generates REST API Documentation from standard input to ' \
        'standard output.'
    __arguments__ = [
        Argument(
            '-f', '--format',
            default='markdown',
            help='The output format. One of markdown, html. Default is '
                'markdown.'
        ),
    ]

    formatters = {
        'markdown': MarkdownFormatter,
        # 'html': HtmlFormatter,
    }

    def __call__(self, args):
        self.convert_file(sys.stdin, sys.stdout, args.format)

    def convert_file(self, source, destination, format):
        from ..authoring import Story
        story = Story.load(source)
        story.document(
            destination,
            formatter_factory=self.formatters[format]
        )


