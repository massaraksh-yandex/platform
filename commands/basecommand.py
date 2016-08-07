from abc import ABCMeta, abstractmethod
from color.color import colored, Color, Style
from params.exception import PlatformException
from params.params import Params


class BaseCommand(metaclass=ABCMeta):
    def __init__(self, parent, database):
        self.parent = parent
        self.database = database

    def path(self, separator=' ') -> str:
        def chain(s):
            ret = [s.name()]
            if s.parent is not None:
                ret = chain(s.parent) + ret
            return ret

        return separator.join(chain(self))

    def execute(self, argv):
        try:
            p = Params(argv)
            if self._need_help(p):
                self._print_help()
            else:
                self._process(p)
        except PlatformException as e:
            self._error(e)
        except Exception:
            raise

    def call_child_cmd(self, cls):
        return cls(self, self.database)

    def about(self) -> str:
        return self._format(self._about())

    def _print_help(self):
        print(self.about())
        print()
        print('Использование:')

        for info in self._additional_info():
            print(info)
            print()

    def _error(self, error):
        message = str(error)
        if message != '':
            print(colored(message, Color.red))
        self._print_help()

    def _check_rules(self, p: Params):
        result = set()
        for l in self._rules():
            res = l.attempt(p)
            if res is not None:
                result.add(res)

        size = len(result)
        if size == 1:
            return result.pop()
        elif size == 0:
            raise PlatformException('Аргументы не подходят ни под одно правило' if len(p.argv) else '')
        else:
            raise PlatformException('Аргументы подходят под несколько правил программы')

    def _format(self, message: str):
        return message.format(path=colored(self.path(), Color.green, Style.underline),
                              name=self.name(), space='\t')

    @abstractmethod
    def name(self) -> '':
        return ''

    @abstractmethod
    def _about(self) -> str:
        return 'information'

    @abstractmethod
    def _process(self, p: Params):
        pass

    @abstractmethod
    def _rules(self) -> []:
        return []

    @abstractmethod
    def _additional_info(self) -> []:
        return []

    @abstractmethod
    def _need_help(self, p: Params):
        pass
