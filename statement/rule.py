from params.params import Params
from statement.check import Check
from statement.empty import Empty
from statement.has import Has
from statement.not_empty import NotEmpty
from statement.size import Size


class Rule:
    def __init__(self, p: Params):
        self.params = p

    def size(self):
        return Size(self)

    def check(self):
        return Check(self)

    def empty(self):
        return Empty(self)

    def not_empty(self):
        return NotEmpty(self)

    def has(self):
        return Has(self)
