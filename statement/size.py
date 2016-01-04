from params.exception import PlatformException


class Size:
    def __init__(self, rule):
        self.rule = rule

    def equals(self, arr, size):
        if len(arr) != size:
            raise PlatformException()
        return self.rule

    def more_or_equals(self, arr, size):
        if len(arr) < size:
            raise PlatformException()
        return self.rule

    def not_equals(self, arr, size):
        if len(arr) == size:
            raise PlatformException()
        return self.rule
