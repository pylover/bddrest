from easycli import Root

from .documentary import DocumentaryLauncher


class BDDRESTCommand(Root):
    __help__ = 'bddrest command line interface.'
    __completion__ = True
    __arguments__ = [
        DocumentaryLauncher,
    ]


def main():
    BDDRESTCommand().main()
