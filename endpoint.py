from abc import abstractmethod
from platform.command import Command
from platform.exception import WrongOptions, WrongTargets, WrongDelimers
from platform.params import Params


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

    def _process(self, p: Params, res):
        res(p)

    def _commands(self) -> {}:
        return {}

    @abstractmethod
    def _help(self) -> []:
        pass

    @abstractmethod
    def _rules(self) -> bool:
        pass