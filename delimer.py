from platform.exception import WrongDelimers

__author__ = 'massaraksh'


class Delimer:
    index = 0
    def __init__(self, index):
        self.index = index


class DoubleDelimer(Delimer):
    def __init__(self, index):
        super().__init__(index)


class SingleDelimer(Delimer):
    def __init__(self, index):
        super().__init__(index)


def checkNoDelimers(p):
    if len(p.delimer) > 0:
        raise WrongDelimers('Разделители не допускаются')