from collections import namedtuple
from os.path import join, pardir, dirname, realpath
from platform.commands.command import Command
from platform.db.config import Config
from platform.utils.utils import importCommands, setupCodecs
import sys


ConfigHooks = namedtuple('ConfigHooks', ['check', 'init', 'save', 'create'])


def main(name, information, hooks = ConfigHooks(check=lambda: True, create=lambda: Config(),
                                   init=lambda: None, save=lambda: None )):
    class MainCommand(Command):
        def __init__(self, name, config):
            super().__init__(None, config)
            self._name = name
            self._realpath = join(__file__, pardir, pardir)
        def name(self):
            return self._name
        def _info(self):
            return information
        def _commands(self):
            realPath = dirname(realpath(self._realpath))
            return importCommands(realPath)

    setupCodecs()

    if not hooks.check():
        hooks.init()
        hooks.save()
    Config.instance = hooks.create()
    MainCommand(name, hooks.create()).execute(sys.argv[1:])
