import sys
import argparse

from .formatters import *
from .documenter import Documenter
from ..cli import Launcher


class DocumentaryLauncher(Launcher):
    formatters = {
        'markdown': MarkdownFormatter,
        # 'html': HtmlFormatter,
    }

    @classmethod
    def create_parser(cls, subparsers):
        parser = subparsers.add_parser(
            'document',
            help='Generates REST API Documentation from standard input to standard output.'
        )
        parser.add_argument(
            '-f',
            '--format',
            default='markdown',
            help='The output format. One of markdown, html. Default is markdown.'
        )
        return parser

    def convert_file(self, source, destination):
        from ..authoring import Story
        story = Story.load(source)
        story.document(destination, formatter_factory=self.formatters[self.args.format])

    def launch(self):
        self.convert_file(sys.stdin, sys.stdout)

