import sys
import argparse
from os import path

import argcomplete


from .launchers import Launcher, RequireSubCommand


class MainLauncher(Launcher):

    def __init__(self):
        self.parser = parser = argparse.ArgumentParser(
            prog=path.basename(sys.argv[0]),
            description='bddrest command line interface.'
        )

        subparsers = parser.add_subparsers(
            title="Sub Commands",
            dest="command"
        )

        from ..documentary import DocumentaryLauncher
        DocumentaryLauncher.register(subparsers)

        argcomplete.autocomplete(parser)

    def launch(self, args=None):
        cli_args = self.parser.parse_args(args if args else None)
        if hasattr(cli_args, 'func'):
            cli_args.func(cli_args)
        else:
            super().launch()


root_launcher = None


def main():
    global root_launcher
    if root_launcher is None:
        root_launcher = MainLauncher()
    return root_launcher()

