from abc import ABCMeta, abstractmethod
from platform.color import colored, Color, Style
from platform.params import Params
from platform.exception import WrongOptions, WrongTargets, WrongDelimers
from platform.utils import recieverOptions


class Command(metaclass=ABCMeta):
    def __init__(self, parent):
        self.parent = parent

    def _printHelp(self, helpStrings):
        map = dict(path=colored(self.path(), Color.green, Style.underline),
                   name=self.name(),
                   space='\t')

        for s in helpStrings:
            print(s.format(**map))

    def _error(self, message):
        print(colored(str(message), Color.red))
        self._printHelp(self._help())

    def _checkRules(self, p: Params):
        rets = set()
        for l in self._rules():
            try:
                rets.add(l(p))
            except Exception:
                pass

        l = len(rets)
        if l == 1:
            return rets.pop()
        elif l == 0:
            raise WrongTargets('Аргументы не подходят ни под одно правило')
        else:
            raise WrongTargets('Аргументы подходят под несколько правил программы')

    def _needHelp(self, p: Params):
        return p._helpOptionIndex is not None and \
               p._helpOptionIndex == 0

    def _execute(self, argv):
        p = Params.make(argv)
        if self._needHelp(p):
            self._printHelp(self._help())
        else:
            func = self._checkRules(p)
            self._process(p, func)

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
        def chain(s):
            ret = [s.name()]
            if s.parent is not None:
                ret = chain(s.parent) + ret
            return ret

        return ' '.join(chain(self))

    @abstractmethod
    def name(self) -> '':
        pass

    @abstractmethod
    def _commands(self) -> {}:
        pass

    def _help(self):
        return ['{path} '+pr(self).name() for k, pr in self._commands().items()]

    def _rules(self):
        return recieverOptions(self._commands())

    def _process(self, p: Params, res):
        self._commands()[res](self).execute(p.argv[1:])
