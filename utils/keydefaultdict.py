from collections import defaultdict


class KeyDefaultDict(defaultdict):
    def __init__(self):
        super().__init__()
        self.default_factory = lambda x: None

    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        else:
            ret = self[key] = self.default_factory(key)
            return ret
