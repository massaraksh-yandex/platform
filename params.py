class Params:
    targets = []
    options = []
    argv = []
    delimer = []
    doubleDelimer = []

    def __init__(self, argv):
        self.argv = argv
        self.targets = []
        self.options = []
        self.delimer = []
        self.doubleDelimer = []

        index = 0
        for arg in argv:
            if arg.startswith('--') and arg != '--':
                self.options.append(arg[2:])
            else:
                if arg == '-':  # -
                    self.delimer.append(index)
                elif arg == '--':
                    self.doubleDelimer.append(index)
                self.targets.append(arg)  # target
            index += 1
