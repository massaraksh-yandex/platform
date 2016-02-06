from statement.statement import Statement, InfoStatement
from statement.rule import Rule


class ExtendedStatementFactory:
    def __init__(self, messages):
        self._array = []
        self.info(messages)

    def statement(self, *messages, result, rule):
        self._array.append(Statement(messages, result, rule))
        return self

    def info(self, *messages):
        self._array.append(InfoStatement(messages))
        return self

    def product(self):
        return self._array


class StatementFactory:
    def __init__(self, *messages):
        self._messages = messages

    def extended(self):
        return ExtendedStatementFactory(self._messages)

    def single_option_command(self, result):
        return [Statement(self._messages, result,
                          rule=lambda p: Rule(p).empty().delimiters()
                                                .empty().options()
                                                .size().equals(p.targets, 1))]

    def empty_command(self, result):
        return [Statement(self._messages, result,
                          rule=lambda p: Rule(p).empty().delimiters()
                                                .empty().options()
                                                .empty().targets())]


def create(*messages):
    return StatementFactory(*messages)
