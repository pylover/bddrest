import sys

from easycli import SubCommand, Argument


class DocumentaryLauncher(SubCommand):
    __command__ = 'document'
    __help__ = 'Generates REST API Documentation from standard input to ' \
        'standard output.'
    __arguments__ = [
        Argument(
            '-f', '--format',
            default='markdown',
            help='The output format. One of markdown or html. Default is '
                 'markdown.'
        ),
    ]

    def __call__(self, args):
        self.convert_file(sys.stdin, sys.stdout, args.format)

    def convert_file(self, source, outfile, format_):
        from ..authoring import Story
        story = Story.load(source)
        story.document(outfile, format_=format_)
