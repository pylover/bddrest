from easycli import Root

from .documentary import DocumentaryLauncher


class Main(Root):
    __help__ = 'bddrest'
    __completion__ = True
    __arguments__ = [
        DocumentaryLauncher
    ]


def main():
    Main()
