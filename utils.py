from os.path import join, basename
from glob import glob
import codecs
import sys


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


def makeCommandDict(commands):
    return { c.name(c): c for c in commands }


def setupCodecs():
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def recieverOptions(map):
    def raiseWrongParsing():
        raise ValueError('Ошибочное условие')

    def inArray(arr, el, message = None):
        if el not in arr:
            m = 'Отсутсвует элемент {0}, получено {1}'.format(el, str(arr))
            raise ValueError(m if message is None else message)
        return True

    return [lambda p: p.argv[0] if inArray(map, p.argv[0]) else raiseWrongParsing()]
