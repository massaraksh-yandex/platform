from params.exception import PlatformException
from params.params import Params
from statement.rule import Rule


class Statement:
    def __init__(self, messages, result, rule):
        self.messages = messages
        self.result = result
        self.rule = rule

    def attempt(self, p: Params):
        try:
            self.rule(p)
        except PlatformException:
            return None
        except IndexError:
            return None

        return self.result


class InfoStatement:
    def __init__(self, messages):
        self.messages = messages

    def attempt(self, p: Params):
        del p
        return None


def empty_command(messages, result):
    return [Statement(messages, result,
                      rule=lambda p: Rule(p).empty().delimiters()
                                            .empty().options()
                                            .empty().targets())]


def single_option_command(messages, result):
    return [Statement(messages, result,
                      rule=lambda p: Rule(p).empty().delimiters()
                                            .empty().options()
                                            .size().equals(p.targets, 1))]
