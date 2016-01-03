class Delimiter(object):
    def __init__(self, index):
        self.index = index


class DoubleDelimiter(Delimiter):
    value = '--'

    def __eq__(self, other):
        return self.value == other.value and self.index == other.index


class SingleDelimiter(Delimiter):
    value = '-'

    def __eq__(self, other):
        return self.value == other.value and self.index == other.index
