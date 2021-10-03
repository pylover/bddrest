from .base import Formatter
from .markdown import MarkdownFormatter
from .html import HTMLFormatter


_formatters = {
    'markdown': MarkdownFormatter,
    'html': HTMLFormatter,
}


def create(format_, outfile, *a, **k):
    return _formatters[format_](outfile, *a, **k)
