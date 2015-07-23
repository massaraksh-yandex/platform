from abc import abstractmethod

from platform.basecommand import BaseCommand
from platform.params import Params
from platform.exception import PlatformException
from platform.statement.statement import Statement, Rule


class Command(BaseCommand):
    def _needHelp(self, p: Params):
        return p.needHelp and len(p.targets) == 0

    def _help(self):
        return []

    def _rules(self) -> []:
        ret = []
        for k, v in self._commands().items():
            ret.append(Statement(['{path} '+v(self).name()], True,
                                 lambda p: Rule(p).notEmpty().targets()
                                                  .check().firstTargetEquality(k)))
        return ret

    def _process(self, p: Params, res):
        self._commands()[p.argv[0]](self).execute(p.argv[1:])

    def _ignoredexceptions(self) -> ():
        return (PlatformException, KeyError)

    @abstractmethod
    def name(self) -> '':
        pass

    @abstractmethod
    def _commands(self) -> {}:
        pass

