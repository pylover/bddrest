from easycli import Root

from .documentary import DocumentaryLauncher
from .mockupserver import MockupServer


class BDDRESTCommand(Root):
    __help__ = 'bddrest'
    __completion__ = True
    __arguments__ = [
        DocumentaryLauncher,
        MockupServer,
    ]


def main():
    BDDRESTCommand().main()
