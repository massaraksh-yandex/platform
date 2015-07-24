from abc import abstractmethod
from platform.command import Command
from platform.basecommand import BaseCommand
from platform.exception import PlatformException
from platform.params import Params


class Endpoint(BaseCommand):
    def _needHelp(self, p: Params):
        return p.needHelp

    def _process(self, p: Params, res):
        res(p)

    def _ignoredexceptions(self) -> ():
        return (PlatformException)

    @abstractmethod
    def name(self) -> '':
        pass

    @abstractmethod
    def _info(self) -> []:
        pass

    @abstractmethod
    def _rules(self) -> []:
        pass
