import params.params
import enum
from params.exception import PlatformException


class Op:
    @staticmethod
    def eq(value):
        def _impl(what):
            return what == value

        return _impl

    @staticmethod
    def not_eq(value):
        def _impl(what):
            return what != value

        return _impl

    @staticmethod
    def more(value, maybe_eq=False):
        def _impl(what):
            return what > value or (what == value if maybe_eq else False)

        return _impl

    @staticmethod
    def less(value, maybe_eq=False):
        def _impl(what):
            return what < value or (what == value if maybe_eq else False)

        return _impl


class Data(enum.Enum):
    Target = 'Target'
    Delimiter = 'Delimiter'
    Option = 'Option'


class Rule:
    def __init__(self):
        self.rules = []

    @staticmethod
    def _get_data(what: Data, p: params.params.Params):
        if what == Data.Target:
            return p.targets
        elif what == Data.Delimiter:
            return p.delimiters
        elif what == Data.Option:
            return p.options
        else:
            raise PlatformException('Unknown Data: ' + str(what))

    def delimiter(self, delimiter):
        def _impl(p: params.params.Params):
            return delimiter in p.delimiters
        self.rules.append(_impl)
        return self

    def target(self, name: str, index: int):
        def _impl(p: params.params.Params):
            if len(p.targets) <= index:
                return False
            return p.targets[index] == params.params.Target(name, index)
        self.rules.append(_impl)
        return self

    def maybe_option(self, name: str, *values):
        def _impl(p: params.params.Params):
            if name in p.options:
                value = p.options[name]
                if value is None and len(values) == 0:
                    return True

                if len(values) == 1 and values[0] == '':
                    return True

                return value in values
            else:
                return True

        self.rules.append(_impl)
        return self

    def option(self, name: str, *values):
        def _impl(p: params.params.Params):
            if name not in p.options:
                return False

            value = p.options[name]
            if value is None and len(values) == 0:
                return True

            if len(values) == 1 and values[0] == '':
                return True

            return value in values
        self.rules.append(_impl)
        return self

    def size(self, what: Data, op):
        def _impl(p: params.params.Params):
            length = len(Rule._get_data(what, p))
            return op(length)
        self.rules.append(_impl)
        return self

    def empty(self, what: Data):
        def _impl(p: params.params.Params):
            length = len(Rule._get_data(what, p))
            return Op.eq(0)(length)
        self.rules.append(_impl)
        return self

    def not_empty(self, what: Data):
        def _impl(p: params.params.Params):
            length = len(Rule._get_data(what, p))
            return Op.not_eq(0)(length)
        self.rules.append(_impl)
        return self

    def has(self, what: Data, value):
        def _impl(p: params.params.Params):
            if what == Data.Target:
                new_value = params.params.Target(value)
            else:
                new_value = value

            data = Rule._get_data(what, p)
            return new_value in data
        self.rules.append(_impl)
        return self

    def __call__(self, p: params.params.Params):
        for rule in self.rules:
            if not rule(p):
                return False
        return True
