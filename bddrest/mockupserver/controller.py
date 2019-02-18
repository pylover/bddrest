from nanohttp import controllers


class MockupController(controllers):

    def __init__(self):
        self.stories = []

    def add_story(self, story):
        self.stories.append(story)

    def __call__(self, *remaining_paths):
        pass

