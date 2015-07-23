from abc import abstractmethod

from platform.basecommand import BaseCommand
from platform.params import Params
from platform.exception import PlatformException
from platform.check import recieverOptions


class Command(BaseCommand):
    def _needHelp(self, p: Params):
        return p.needHelp and len(p.targets) == 0

    def _help(self):
        return ['{path} '+pr(self).name() for k, pr in self._commands().items()]

    def _rules(self) -> []:
        return recieverOptions(self._commands())

    def _process(self, p: Params, res):
        self._commands()[res](self).execute(p.argv[1:])

    def _ignoredexceptions(self) -> ():
        return (PlatformException, KeyError)

    @abstractmethod
    def name(self) -> '':
        pass

    @abstractmethod
    def _commands(self) -> {}:
        pass

