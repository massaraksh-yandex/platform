from os.path import join, pardir, dirname, realpath
from commands.command import Command
from db.database import Database
from utils.utils import _import_commands, _setup_codecs
import sys


def main(name, information, scheme):
    class MainCommand(Command):
        def __init__(self):
            super().__init__(None, Database(scheme))

        def name(self):
            return name

        def _about(self):
            return information

        def _sub_commands(self):
            real_path = dirname(realpath(join(__file__, pardir, pardir)))
            return [v for k, v in _import_commands(real_path).items()]

    _setup_codecs()

    MainCommand().execute(sys.argv[1:])
