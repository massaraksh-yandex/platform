class Delimer(object):
    def __init__(self, index):
        self.index = index


class DoubleDelimer(Delimer):
    def __init__(self, index):
        super().__init__(index)


class SingleDelimer(Delimer):
    def __init__(self, index):
        super().__init__(index)