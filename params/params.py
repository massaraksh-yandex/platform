import re
from collections import namedtuple
from params.delimiter import SingleDelimiter, DoubleDelimiter
from params.exception import WrongDelimiters
from utils.keydefaultdict import KeyDefaultDict


class Target:
    Empty = -1

    def __init__(self, value='', index=Empty):
        self.value = value
        self.index = index

    def __eq__(self, other):
        ret = self.value == other.value
        if self.index != Target.Empty and other.index != Target.Empty:
            ret = ret and self.index == other.index
        return ret



class Params:
    def __init__(self, args):
        self.argv = args
        self.options = KeyDefaultDict()
        self.targets = []
        self.delimiters = []

        r = re.compile('\-+$')
        index = 0
        for arg in self.argv:
            if Params._is_delimiter(r, arg):
                self.delimiters.append(Params._create_delimiter(arg, index))
            elif Params._is_option(arg):
                k, v = Params._parse_option(arg)
                self.options[k] = v
            elif arg:
                self.targets.append(Target(arg, index))
                index += 1

        self.needHelp = 'help' in self.options

        last = 0
        self.separated = []
        for d in self.delimiters:
            self.separated.append(self.targets[last:d.index])
            last = d.index
        self.separated.append(self.targets[last:])

    @staticmethod
    def _is_option(arg):
        return arg.startswith('--') and arg != '--'

    @staticmethod
    def _is_delimiter(reg, arg):
        return reg.match(arg)

    @staticmethod
    def _create_delimiter(delimiter, index):
        if delimiter == SingleDelimiter.etalon:
            return SingleDelimiter(index)
        elif delimiter == DoubleDelimiter.etalon:
            return DoubleDelimiter(index)
        else:
            raise WrongDelimiters('Не могу создать разделитель: {0}, {1}'.format(delimiter, index))

    @staticmethod
    def _parse_option(arg):
        opt = arg[2:].split('=', 1)
        return opt[0], None if len(opt) == 1 else opt[1]
