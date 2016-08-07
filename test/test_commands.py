import unittest
from commands.command import Command
from commands.endpoint import Endpoint
from params.params import Params
from statement.create import create
from statement.rule import Rule, Data, Op


class MethodWasCalled(Exception):
    pass


_help = {
    'first': 'first.help',
    'second': 'second.help',
    'third': 'third.help',
    'scope': 'scope.help\nsecond line',
    'root': 'root.help'
}


class Db:
    val = ''

    def assign(self, new_val):
        self.val = new_val


class First(Endpoint):
    def name(self):
        return 'first'

    def _about(self):
        return _help[self.name()]

    def _rules(self):
        return create('first info line\n' +
                      'second info line').empty_command(self.hook)

    def hook(self, p: Params):
        self.database.assign('First.hook')


class Second(Endpoint):
    def name(self):
        return 'second'

    def _about(self):
        return _help[self.name()]

    def _rules(self):
        return create('adf').single_option_command(self.hook)

    def hook(self, p: Params):
        self.database.assign('Second.hook')


class Third(Endpoint):
    def name(self):
        return 'third'

    def _about(self):
        return _help[self.name()]

    def _rules(self):
        return create('extended rule').extended()\
            .statement('flag', result=self.hook,
                       rule=Rule().empty(Data.Delimiter)
                                  .empty(Data.Target)
                                  .option('flag'))\
            .info('second info message\nmultiline')\
            .statement('target', result=self.another_hook,
                       rule=Rule().empty(Data.Delimiter)
                                  .empty(Data.Option)
                                  .size(Data.Target, Op.eq(1)))\
            .product()

    def hook(self, p: Params):
        self.database.assign('Third.hook')

    def another_hook(self, p: Params):
        self.database.assign('Third.another_hook')


class Scope(Command):
    def name(self):
        return 'scope'

    def _about(self):
        return _help[self.name()]

    def _sub_commands(self):
        return [Second, Third]


class Root(Command):
    def name(self):
        return 'root'

    def _about(self):
        return _help[self.name()]

    def _sub_commands(self):
        return [First, Scope]


class TestCommands(unittest.TestCase):
    def setUp(self):
        self.root = Root(None, None)

        self.cases = [
            ('', ''),
            ('first', 'First.hook'),
            ('scope second target', 'Second.hook'),
            ('scope third target', 'Third.another_hook'),
            ('scope third --flag', 'Third.hook')
        ]

    def _impl(self, args, expected):
        try:
            self.root.execute(args)
        except MethodWasCalled as e:
            self.assertEqual(str(e), expected)

    def test_check_all(self):
        for case in self.cases:
            args = case[0]

            db = Db()
            root = Root(None, db)

            root.execute(args.split(' '))
            self.assertEqual(db.val, case[1])

    def test_path(self):
        db = Db()
        root = Root(None, db)

        self.assertEqual(root.path(), 'root')
        self.assertEqual(root.call_child_cmd(First).path(), 'root first')
        self.assertEqual(root.call_child_cmd(Scope).path(), 'root scope')
        self.assertEqual(root.call_child_cmd(Scope).call_child_cmd(Second).path(separator='.'), 'root.scope.second')
        self.assertEqual(root.call_child_cmd(Scope).call_child_cmd(Third).path(separator='-'), 'root-scope-third')
