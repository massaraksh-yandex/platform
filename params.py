from platform.delimer import DoubleDelimer, SingleDelimer
from platform.exception import WrongOptions


class Params:
    def __init__(self):
        self.argv = []
        self.delimer = []
        self.targets = []
        self.options = {}
        self._helpOptionIndex = None

    @staticmethod
    def make(args):
        def checkDobuleDelimer(arg):
            return arg == '--'

        def checkSingleDelimer(arg):
            return arg == '-'

        def isOption(arg):
            return arg.startswith('--') and arg != '--'

        def parseOption(arg):
            opt = arg[2:].split('=', 1)
            if len(opt) == 1:
                return (opt[0], None)

            if opt[1].startswith('\'') and opt[1].endswith('\''):
                opt[1] = opt[1][1:-1]

            return (opt[0], opt[1])

        p = Params()
        p.argv = args
        passedTargets = 0
        iter = 0
        for arg in args:
            if isOption(arg):
                opt = arg[2:]
                if opt == 'help':
                    p._helpOptionIndex = iter
                else:
                    k, v = parseOption(arg)
                    if k in p.options:
                        raise WrongOptions('Дублирующаяся опция: {0}'.format(k))
                    p.options[k] = v
            else:
                if checkDobuleDelimer(arg):
                    p.delimer.append(DoubleDelimer(passedTargets))
                elif checkSingleDelimer(arg):
                    p.delimer.append(SingleDelimer(passedTargets))
                else:
                    p.targets.append(arg)
                passedTargets += 1
            iter += 1
        return p
