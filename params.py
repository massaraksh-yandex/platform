from platform.delimer import DoubleDelimer, SingleDelimer
from platform.exception import WrongOptions


class Params:
    argv = None
    delimer = None
    targets = None
    options = None

    _helpOptionIndex = None

    def __init__(self):
        self.argv = []
        self.delimer = []
        self.targets = []
        self.options = {}

def makeParams(args) -> Params:
    def checkDobuleDelimer(arg):
        return arg == '--'

    def checkSingleDelimer(arg):
        return arg == '-'

    def isOption(arg):
        return arg.startswith('--') and arg != '--'

    def parseOption(arg):
        ind = arg.find('=')
        if ind == -1:
            return (arg[2:], '')
        return (arg[2:ind], arg[ind:])

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
