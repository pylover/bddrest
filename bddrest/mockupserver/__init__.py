import sys


from easycli import SubCommand, Argument


class MockupServer(SubCommand):
    __command__ = 'mockupserver'

    def __call__(self, args):
        print("ok")

