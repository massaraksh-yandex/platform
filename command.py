from platform.params import makeParams, Params
from platform.exception import WrongOptions, WrongTargets, WrongDelimers


class Command:
    parent = None

    def __init__(self, parent):
        self.parent = parent

    def _chain(self):
        ret = [self.name()]
        if self.parent is not None:
            ret = self.parent._chain() + ret
        return ret

    def _printHelp(self, helpStrings):
        for s in helpStrings:
            print(s.format(path=self.path(), name=self.name()))

    def _error(self, message):
        print(message)
        print('\n')
        self._printHelp(self._help())

    def _needHelp(self, p: Params):
        return p._helpOptionIndex is not None and \
               p._helpOptionIndex == 0

    def _execute(self, argv):
        p = makeParams(argv)
        if self._needHelp(p):
            self._printHelp(self._help())
        else:
            self._check(p)
            self._process(p)

    def execute(self, argv):
        try:
            self._execute(argv)
        except WrongOptions as e:
            self._error(e)
        except WrongTargets as e:
            self._error(e)
        except WrongDelimers as e:
            self._error(e)
        except KeyError as e:
            self._error(e)

    def path(self):
        return ' '.join(self._chain())

    def name(self):
        raise NotImplementedError('name() -> string is not implemented')

    def _help(self):
        raise NotImplementedError('_help() -> [] is not implemented')

    def _check(self, p: Params):
        raise NotImplementedError('_check() -> bool is not implemented')

    def _process(self, p: Params):
        raise NotImplementedError('_process() -> void is not implemented')


class Endpoint(Command):
    def __init__(self, parent):
        super().__init__(parent)

    def _needHelp(self, p: Params):
        return p._helpOptionIndex is not None

    def execute(self, argv): # do not catch KeyError
        try:
            self._execute(argv)
        except WrongOptions as e:
            self._error(e)
        except WrongTargets as e:
            self._error(e)
        except WrongDelimers as e:
            self._error(e)
