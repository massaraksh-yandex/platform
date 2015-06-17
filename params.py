from platform.delimer import DoubleDelimer, SingleDelimer
from platform.exception import WrongOptions
from platform.keydefaultdict import keydefaultdict


class Params:
    def __init__(self):
        self.argv = []
        self.delimer = []
        self.targets = []
        self.options = keydefaultdict(lambda x: None)
        self._helpOptionIndex = None

    @staticmethod
    def _checkDobuleDelimer(arg):
        return arg == '--'

    @staticmethod
    def _checkSingleDelimer(arg):
        return arg == '-'

    @staticmethod
    def _parseOption(arg):
        opt = arg[2:].split('=', 1)
        return (opt[0], None if len(opt) == 1 else opt[1])

    @staticmethod
    def isOption(arg):
        return arg.startswith('--') and arg != '--'

    @staticmethod
    def parseOption(arg):
        if Params.isOption(arg):
            k, v = Params._parseOption(arg)
            return (k, v)
        else:
            raise WrongOptions('Опция {0} не распарсилась'.format(arg))

    @staticmethod
    def makeRawParams(args):
        p = Params()

        if len(args) > 0:
            arg = args[0]
            if Params.isOption(arg):
                opt = arg[2:]
                if opt == 'help':
                    p._helpOptionIndex = 0

        p.argv = args
        return p

    @staticmethod
    def parse(args):
        if isinstance(args, Params):
            return args

        p = Params()
        p.argv = args
        passedTargets = 0
        iter = 0
        for arg in args:
            if Params.isOption(arg):
                opt = arg[2:]
                if opt == 'help':
                    p._helpOptionIndex = iter
                else:
                    k, v = Params._parseOption(arg)
                    if k in p.options:
                        raise WrongOptions('Дублирующаяся опция: {0}'.format(k))
                    p.options[k] = v
            else:
                if Params._checkDobuleDelimer(arg):
                    p.delimer.append(DoubleDelimer(passedTargets))
                elif Params._checkSingleDelimer(arg):
                    p.delimer.append(SingleDelimer(passedTargets))
                else:
                    p.targets.append(arg)
                passedTargets += 1
            iter += 1
        return p
