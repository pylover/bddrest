
from .helpers import ObjectProxy
from .specification import Call, Story, OverriddenCall, VerifyError
from .authoring import Given, ComposingMixin, When, ComposingCall
# from .documentary import DocumentGenerator, Formatter, MarkdownFormatter

__version__ = '0.3.1a1.dev4'


story = ObjectProxy(Given.get_current)
response = ObjectProxy(lambda: story.current_call.response)


def given(application, *args, **kwargs):
    return Given(application, *args, **kwargs)


def when(*args, **kwargs):
    story.when(*args, **kwargs)


def then(*args, **kwargs):
    story.then(*args, **kwargs)


and_ = then


# TODO: Move it to cli package
# def generate_documents(directory):
#     doc = DocumentGenerator(
#         formatter=MarkdownFormatter(),
#         output_directory='<TODO:>',
#     )
#     for spec in directory:
#         doc.generate(spec)
