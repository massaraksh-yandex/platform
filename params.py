from platform.delimer import DoubleDelimer, SingleDelimer

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
        self.options = []

def makeParams(args) -> Params:
    def checkDobuleDelimer(arg):
        return arg == '--'

    def checkSingleDelimer(arg):
        return arg == '-'

    def isOption(arg):
        return arg.startswith('--') and arg != '--'

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
                p.options.append(opt)
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
