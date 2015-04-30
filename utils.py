from os.path import join, basename
from glob import glob
import sys


def importCommands(path):
    commandsPath = join(path, 'commands')
    sys.path.append(commandsPath)
    commands = {}
    for name in glob(commandsPath + '/*.py'):
        module = __import__(basename(name[:-3]), globals(), locals())

        for command in module.module_commands.keys():
            commands[command] = module.module_commands[command]

    return commands