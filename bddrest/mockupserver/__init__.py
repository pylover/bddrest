import sys

from easycli import SubCommand, Argument
#from bddrest.mockupserver.controller import MockupController


class MockupServer(SubCommand):
    __command__ = 'mockupserver'
    __help__ = 'Generates a mockup from YAML file.'
    __arguments__ = [
        Argument(
            'story',
            metavar='YAML',
            help='A story file'
        ),
    ]

    def __call__(self, args):
        from ..authoring import Story
        with open(args.story) as story_file:
            story = Story.load(story_file)
            print(story.base_call.url)
        server = MockupController()
        print(server.__call__(story.base_call))



