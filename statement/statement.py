from params.params import Params


class Statement:
    def __init__(self, message, result, rule):
        self.message = message
        self.result = result
        self.rule = rule

    def attempt(self, p: Params):
        ret = self.rule(p)

        if ret:
            return self.result
        else:
            return None


class InfoStatement:
    def __init__(self, message):
        self.message = message

    def attempt(self, p: Params):
        del p
        return None
