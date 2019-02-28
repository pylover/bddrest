import sys
import json

from easycli import SubCommand, Argument
from nanohttp import Controller, HTTPNotFound, context


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

        class RootMockupController(Controller):

            def __init__(self):
                self.stories = []

            def add_story(self, story):
                self.stories.append(story)

            def server(self, call):
                for k, v in call.response.headers:
                    context.response_headers.add_header(k, v)
                yield call.response.text.encode()

            def __call__(self, *remaining_paths):
                calls = [story.base_call] + story.calls
                for call in calls:
                    url = call.url.replace(':', '')
                    if set(url.strip('/').split('/')) == set(remaining_paths) :
                        return self.server(call)
                raise HTTPNotFound()

        from nanohttp import quickstart
        quickstart(RootMockupController())
