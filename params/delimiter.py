class Delimiter(object):
    Empty = -1

    def __init__(self, value, index):
        self.index = index
        self.value = value

    def __eq__(self, other):
        ret = self.value == other.value
        if self.index != Delimiter.Empty and other.index != Delimiter.Empty:
            ret = ret and self.index == other.index
        return ret


class DoubleDelimiter(Delimiter):
    etalon = '--'

    def __init__(self, index=Delimiter.Empty):
        super().__init__(DoubleDelimiter.etalon, index)


class SingleDelimiter(Delimiter):
    etalon = '-'

    def __init__(self, index=Delimiter.Empty):
        super().__init__(SingleDelimiter.etalon, index)
