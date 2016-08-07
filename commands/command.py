from abc import abstractmethod
from commands.basecommand import BaseCommand
from params.params import Params
from params.exception import PlatformException


def _command_map(commands):
    return {c.name(c): c for c in commands}


class Command(BaseCommand):
    def _need_help(self, p: Params):
        return p.needHelp and len(p.targets) == 0

    def _rules(self) -> []:
        return []

    def _process(self, p: Params):
        if len(p.argv) == 0:
            self._print_help()
            return

        cmd = p.argv[0]
        command_dict = _command_map(self._sub_commands())

        if cmd == '':
            self._print_help()
        else:
            if cmd not in command_dict:
                raise PlatformException('Такой подкоманды нет: '+cmd)

            self.call_child_cmd(command_dict[cmd]).execute(p.argv[1:])

    def _additional_info(self) -> []:
        return [self.call_child_cmd(cmd).about() for cmd in self._sub_commands()]

    @abstractmethod
    def name(self) -> '':
        pass

    @abstractmethod
    def _about(self) -> str:
        pass

    @abstractmethod
    def _sub_commands(self) -> []:
        pass
