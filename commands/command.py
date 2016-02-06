from abc import abstractmethod
from commands.basecommand import BaseCommand
from params.params import Params
from params.exception import PlatformException
from statement.statement import Statement
from statement.rule import Rule


def _command_map(commands):
    return {c.name(c): c for c in commands}


class Command(BaseCommand):
    def _need_help(self, p: Params):
        return p.needHelp and len(p.targets) == 0

    def _rules(self) -> []:
        def command_rule(p):
            return Rule(p).not_empty().targets().check().target(0, name)

        ret = []
        command_dict = _command_map(self._sub_commands())

        for name, command_type in command_dict.items():
            cmd = command_type(self, self.database)
            formatted_about = cmd._list_to_message(cmd._about())

            ret.append(Statement(formatted_about, True, command_rule))

        return ret

    def _process(self, p: Params):
        command_dict = _command_map(self._sub_commands())
        self.call_child_cmd(command_dict[p.argv[0]]).execute(p.argv[1:])

    def _ignored_exceptions(self) -> ():
        return PlatformException, KeyError

    @abstractmethod
    def name(self) -> '':
        return ''

    @abstractmethod
    def _about(self) -> []:
        return ['information']

    @abstractmethod
    def _sub_commands(self) -> []:
        return []
