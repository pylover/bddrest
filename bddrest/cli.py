from easycli import Root

from .documentary import DocumentaryLauncher
from .mockupserver import MockupServer

class Main(Root):
    __help__ = 'bddrest'
    __completion__ = True
    __arguments__ = [
        DocumentaryLauncher,
        MockupServer,
    ]

