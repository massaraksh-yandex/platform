from statement.statement import Statement, InfoStatement
from statement.rule import Rule, Op, Data


class ExtendedStatementFactory:
    def __init__(self, message):
        self._array = []
        self.info(message)

    def statement(self, *messages, result, rule):
        self._array.append(Statement('\n'.join(messages), result, rule))
        return self

    def info(self, message):
        self._array.append(InfoStatement(message))
        return self

    def product(self):
        return self._array


class StatementFactory:
    def __init__(self, messages):
        self._messages = messages

    def extended(self):
        return ExtendedStatementFactory(self._messages)

    def single_option_command(self, result):
        return [Statement(self._messages, result,
                          rule=Rule().empty(Data.Delimiter)
                                     .empty(Data.Option)
                                     .size(Data.Target, Op.eq(1)))]

    def empty_command(self, result):
        return [Statement(self._messages, result,
                          rule=Rule().empty(Data.Delimiter)
                                     .empty(Data.Option)
                                     .empty(Data.Target))]


def create(message):
    return StatementFactory(message)
