import sys

from .formatters import *
from .documenter import Documenter
from easycli import SubCommand, Argument


class DocumentaryLauncher(SubCommand):
    __command__ = 'document'
    __arguments__ = [
        Argument(
            '-f', '--format',
            default='markdown',
            help='The output format. One of markdown, html. Default is '
                'markdown.'
        ),
        Argument(
            'document',
            help='Generates REST API Documentation from standard input to '
                'standard output.'
        )
    ]

    formatters = {
        'markdown': MarkdownFormatter,
        # 'html': HtmlFormatter,
    }

    def __call__(self):
        self.convert_file(sys.stdin, sys.stdout)

    def convert_file(self, source, destination):
        from ..authoring import Story
        story = Story.load(source)
        story.document(
            destination,
            formatter_factory=self.formatters[self.args.format]
        )


