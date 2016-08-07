import unittest
from params.params import Params, Target
from params.delimiter import SingleDelimiter, DoubleDelimiter
from params.exception import WrongDelimiters


class TestTargets(unittest.TestCase):
    def test_simple(self):
        args = ['target0', 'target1']
        p = Params(args)

        self.assertEqual(len(args), len(p.targets))
        self.assertEqual(p.targets[0], Target('target0', 0))
        self.assertEqual(p.targets[1], Target('target1', 1))

    def test_empty(self):
        args = ['']
        p = Params(args)

        self.assertEqual(0, len(p.targets))

        args = ['--option', '--']
        p = Params(args)

        self.assertEqual(0, len(p.targets))


class TestOptions(unittest.TestCase):
    def test_simple(self):
        args = ['--flag', '--key=value', '--key2=value 2']
        p = Params(args)

        self.assertEqual(len(args), len(p.options))
        self.assertEqual(p.options['flag'], None)
        self.assertEqual(p.options['key'], 'value')
        self.assertEqual(p.options['key2'], 'value 2')

    def test_equals(self):
        args = ['--key=value', '--key=value2']
        p = Params(args)

        self.assertEqual(len(p.options), 1)
        self.assertEqual(p.options['key'], 'value2')

    def test_empty(self):
        args = ['target']
        p = Params(args)

        self.assertEqual(0, len(p.options))

    def test_help(self):
        args = ['--help']
        p = Params(args)

        self.assertTrue('help' in p.options)
        self.assertTrue(p.needHelp)

    def test_not_help(self):
        args = ['--not_help']
        p = Params(args)

        self.assertTrue('not_help' in p.options)
        self.assertFalse(p.needHelp)


class TestDelimiters(unittest.TestCase):
    def test_type(self):
        args = ['-', '--', '-', '--']
        p = Params(args)
        expected = [SingleDelimiter(0), DoubleDelimiter(0), SingleDelimiter(0), DoubleDelimiter(0)]

        self.assertListEqual(p.delimiters, expected)

    def test_position(self):
        args = ['first', '-', 'second', '--', 'third', 'fourth', '--', 'fifth']
        p = Params(args)
        expected = [SingleDelimiter(1), DoubleDelimiter(2), DoubleDelimiter(4)]

        self.assertListEqual(p.delimiters, expected)

    def test_wrong_delimiter(self):
        args = ['-', '--', '---']
        self.assertRaises(WrongDelimiters, Params, args)


class TestSeparated(unittest.TestCase):
    def test_simple(self):
        args = ['first', '-', 'second', '--', 'third', 'fourth', '--', 'fifth']
        p = Params(args)

        expected = [
            [Target('first', 0)],
            [Target('second', 1)],
            [Target('third', 2), Target('fourth', 3)],
            [Target('fifth', 4)]
        ]

        self.assertListEqual(p.separated, expected)


class TestComplex(unittest.TestCase):
    def setUp(self):
        args = ['first', '-', '--key=value',
                'second', '--key=value2', '--help', '--help=some information', '--',
                'third', '--flag',
                'fourth', '--',
                'fifth']

        self.p = Params(args)

        self.expected = {
            'targets': [
                Target('first', 0),
                Target('second', 1),
                Target('third', 2),
                Target('fourth', 3),
                Target('fifth', 4)
            ], 'options': [
                ('key', 'value2'),
                ('flag', None),
                ('help', 'some information')
            ], 'delimiters': [
                SingleDelimiter(1),
                DoubleDelimiter(2),
                DoubleDelimiter(4)
            ], 'help': 'some information'
            , 'separated': [
                [Target('first', 0)],
                [Target('second', 1)],
                [Target('third', 2), Target('fourth', 3)],
                [Target('fifth', 4)]
            ]
        }

    def test_targets(self):
        self.assertListEqual(self.p.targets, self.expected['targets'])

    def test_options(self):
        opts = self.expected['options']

        self.assertEqual(len(opts), len(self.p.options))
        for o in opts:
            self.assertEqual(o[1], self.p.options[o[0]])

    def test_delimiters(self):
        self.assertEqual(self.p.targets, self.expected['targets'])

    def test_help(self):
        self.assertTrue(self.p.needHelp)
        self.assertEqual(self.p.options['help'], self.expected['help'])

    def test_separated(self):
        self.assertListEqual(self.p.separated, self.expected['separated'])
