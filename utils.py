from os.path import dirname, realpath, pardir, join, basename
from glob import glob
import sys
import io
from platform.config import Config
from platform.command import Command
from collections import namedtuple

ConfigHooks = namedtuple('ConfigHooks', ['check', 'init', 'save', 'create'])

def importCommands(path):
    commandsPath = join(path, 'commands')
    sys.path.append(commandsPath)
    commands = {}
    for name in glob(commandsPath + '/*.py'):
        module = __import__(basename(name[:-3]), globals(), locals())

        try:
            for command in module.module_commands.keys():
                commands[command] = module.module_commands[command]
        except AttributeError:
            pass

    return commands


def makeCommandDict(*commands):
    return { c.name(c): c for c in commands }


def main(name, information, hooks = ConfigHooks(check=lambda: True, create=lambda: Config(),
                                   init=lambda: None, save=lambda: None )):
    class MainCommand(Command):
        def __init__(self, name):
            super().__init__(None)
            self._name = name
            self._realpath = join(__file__, pardir)
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
    MainCommand(name).execute(sys.argv[1:])



def setupCodecs():
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering = True)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', line_buffering = True)
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
