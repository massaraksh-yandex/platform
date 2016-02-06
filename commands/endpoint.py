from abc import abstractmethod
from commands.basecommand import BaseCommand
from params.exception import PlatformException
from params.params import Params


class Endpoint(BaseCommand):
    def _need_help(self, p: Params):
        return p.needHelp

    def _process(self, p: Params):
        res = self._check_rules(p)
        res(p)

    def _ignored_exceptions(self) -> ():
        return PlatformException

    @abstractmethod
    def name(self) -> '':
        pass

    @abstractmethod
    def _about(self) -> []:
        pass

    @abstractmethod
    def _rules(self) -> []:
        pass
