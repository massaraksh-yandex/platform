from abc import ABCMeta, abstractmethod
from platform.color import colored, Color, Style
from platform.exception import PlatformException
from platform.params import Params


class BaseCommand(metaclass=ABCMeta):
    def __init__(self, parent):
        self.parent = parent

    def path(self, separator = ' ') -> str:
        def chain(s):
            ret = [s.name()]
            if s.parent is not None:
                ret = chain(s.parent) + ret
            return ret

        return separator.join(chain(self))

    def execute(self, argv):
        try:
            self._execute(argv)
        except Exception as e:
            if isinstance(e, self._ignoredexceptions()):
                self._error(e)
            else:
                raise

    def _execute(self, argv):
        p = Params(argv)
        if self._needHelp(p):
            self._printHelp()
        else:
            self._process(p, self._checkRules(p))

    def _printHelp(self):
        map = dict(path=colored(self.path(), Color.green, Style.underline),
                   name=self.name(),
                   space='\t')

        for s in self._help():
            print(s.format(**map))

        for l in self._rules():
            for s in l.messages:
                print(s.format(**map))

    def _error(self, message):
        print(colored(str(message), Color.red))
        self._printHelp()

    def _checkselectedrule(self, ruleset: set, p: Params):
        l = len(ruleset)
        if l == 1:
            return ruleset.pop()
        elif l == 0:
            raise PlatformException('Аргументы не подходят ни под одно правило' if len(p.argv) else '')
        else:
            raise PlatformException('Аргументы подходят под несколько правил программы')

    def _checkRules(self, p: Params):
        rets = set()
        for l in self._rules():
            res = l.attempt(p)
            if res is not None:
                rets.add(res)

        return self._checkselectedrule(rets, p)

    @abstractmethod
    def name(self) -> '':
        pass

    @abstractmethod
    def _help(self) -> []:
        pass

    @abstractmethod
    def _process(self, p: Params, res):
        pass

    @abstractmethod
    def _rules(self) -> []:
        pass

    @abstractmethod
    def _ignoredexceptions(self) -> ():
        pass

    @abstractmethod
    def _needHelp(self, p: Params):
        pass