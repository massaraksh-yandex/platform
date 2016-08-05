from collections import defaultdict


class KeyDefaultDict(defaultdict):
    def __missing__(self, key=lambda x: None):
        if self.default_factory is None:
            raise KeyError(key)
        else:
            ret = self[key] = self.default_factory(key)
            return ret
