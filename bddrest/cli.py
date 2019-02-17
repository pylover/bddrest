from easycli import Root

from .documentary import DocumentaryLauncher
<<<<<<< HEAD
from .mockupserver import MockupServer
=======
>>>>>>> Migrated to easycli (#51)

class Main(Root):
    __help__ = 'bddrest'
    __completion__ = True
    __arguments__ = [
<<<<<<< HEAD
        DocumentaryLauncher,
        MockupServer,
=======
        DocumentaryLauncher
>>>>>>> Migrated to easycli (#51)
    ]

