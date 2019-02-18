import sys
from contextlib import contextmanager

from bddrest.authoring import when, status, response, given
from easycli import SubCommand, Argument
from nanohttp.controllers import RegexRouteController
#from restfulpy.application import Application

story = None

class MockupServer(SubCommand):
    __command__ = 'mockupserver'
    __arguments__ = [
        Argument(
            'story',
            metavar='YAML',
            help='A story file'
        )
    ]

    def __call__(self, args):
        from ..authoring import Story
        with open(args.story) as story_file:
            story = Story.load(story_file)
            print(story.base_call.url)




