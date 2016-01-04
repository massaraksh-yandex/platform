import unittest
from statement.statement import Statement, InfoStatement, empty_command, single_option_command
from statement.rule import Rule
from params.params import Params
from params.delimiter import SingleDelimiter, DoubleDelimiter
from params.exception import WrongDelimiters, WrongOptions, WrongTargets, PlatformException


RESULT = 42


class TestCheck(unittest.TestCase):
    def setUp(self):
        self.p = Params(['target', '--', '--flag', '--key=value'])

    def test_delimiters_type(self):
        Rule(self.p).check().delimiters_type(DoubleDelimiter)
        self.assertRaises(WrongDelimiters,
                          lambda p: Rule(p).check().delimiters_type(SingleDelimiter), self.p)

    def test_options(self):
        Rule(self.p).check().option_names_in_set('flag', 'key')
        self.assertRaises(WrongOptions,
                          lambda p: Rule(p).check().option_names_in_set('wrong'), self.p)

    def option_value_in_set(self):
        Rule(self.p).check().option_value_in_set('key', 'value')
        self.assertRaises(WrongOptions,
                          lambda p: Rule(p).check().option_names_in_set('key', 'wrong'), self.p)
        self.assertRaises(WrongOptions,
                          lambda p: Rule(p).check().option_names_in_set('wrong', 'value'), self.p)


class TempEmptyAndNotEmpty(unittest.TestCase):
    def setUp(self):
        self.empty = Params([])
        self.not_empty = Params(['target', '--flag', '--'])

    def test_options(self):
        Rule(self.empty).empty().options()
        Rule(self.not_empty).not_empty().options()

        self.assertRaises(WrongOptions,
                          lambda p: Rule(p).empty().options(), self.not_empty)

        self.assertRaises(WrongOptions,
                          lambda p: Rule(p).not_empty().options(), self.empty)

    def test_targets(self):
        Rule(self.empty).empty().targets()
        Rule(self.not_empty).not_empty().targets()

        self.assertRaises(WrongTargets,
                          lambda p: Rule(p).empty().targets(), self.not_empty)

        self.assertRaises(WrongTargets,
                          lambda p: Rule(p).not_empty().targets(), self.empty)

    def test_delimiters(self):
        Rule(self.empty).empty().delimiters()
        Rule(self.not_empty).not_empty().delimiters()

        self.assertRaises(WrongDelimiters,
                          lambda p: Rule(p).empty().delimiters(), self.not_empty)

        self.assertRaises(WrongDelimiters,
                          lambda p: Rule(p).not_empty().delimiters(), self.empty)

    def test_array(self):
        Rule(self.empty).empty().array([])
        Rule(self.not_empty).not_empty().array([''])

        self.assertRaises(PlatformException,
                          lambda p: Rule(p).empty().array(['']), self.not_empty)

        self.assertRaises(PlatformException,
                          lambda p: Rule(p).not_empty().array([]), self.empty)


class TestHas(unittest.TestCase):
    def setUp(self):
        self.p = Params(['--flag'])

    def test_option(self):
        Rule(self.p).has().option('flag')
        self.assertRaises(WrongOptions,
                          lambda p: Rule(p).has().option('wrong'), self.p)

    def test_in_array(self):
        Rule(self.p).has().in_array(['flag', 'target'], 'target')
        self.assertRaises(PlatformException,
                          lambda p: Rule(p).has().in_array(['flag', 'target'], 'wrong'), self.p)


class TestSize(unittest.TestCase):
    def setUp(self):
        self.p = Params([])

    def test_equals(self):
        Rule(self.p).size().equals(['1', '2'], 2)
        self.assertRaises(PlatformException,
                          lambda p: Rule(p).size().equals(['1', '2'], 3), self.p)

    def test_not_equals(self):
        Rule(self.p).size().not_equals(['1', '2'], 3)
        self.assertRaises(PlatformException,
                          lambda p: Rule(p).size().not_equals(['1', '2'], 2), self.p)

    def test_more_or_equals(self):
        Rule(self.p).size().more_or_equals(['1', '2'], 2)
        Rule(self.p).size().more_or_equals(['1', '2'], 1)
        self.assertRaises(PlatformException,
                          lambda p: Rule(p).size().more_or_equals(['1', '2'], 3), self.p)


class TestStatement(unittest.TestCase):
    def test_info_statement(self):
        self.assertEqual(None, InfoStatement('message').attempt(Params([])))
        self.assertEqual(None, InfoStatement('message').attempt(Params(['target', '--flga', '--'])))

    def test_empty_command(self):
        empty_command('message', RESULT)[0].attempt(Params([]))
        self.assertEqual(None, empty_command('message', RESULT)[0].attempt(Params(['target'])))
        self.assertEqual(None, empty_command('message', RESULT)[0].attempt(Params(['--flag'])))
        self.assertEqual(None, empty_command('message', RESULT)[0].attempt(Params(['--'])))

    def test_single_option_command(self):
        single_option_command('message', RESULT)[0].attempt(Params(['target']))
        self.assertEqual(None, single_option_command('message', RESULT)[0].attempt(Params([])))
        self.assertEqual(None, single_option_command('message', RESULT)[0].attempt(Params(['--flag'])))
        self.assertEqual(None, single_option_command('message', RESULT)[0].attempt(Params(['--'])))

    def test_complex1(self):
        p = Params(['target', '--', '--flag', '--key=value'])
        s = Statement('message', RESULT,
                      lambda x: Rule(x).check().delimiters_type(DoubleDelimiter)
                                       .check().option_names_in_set('flag', 'key')
                                       .check().option_value_in_set('key', 'value')
                                       .check().target(0, 'target'))

        self.assertEqual(s.attempt(p), RESULT)

    def test_complex2(self):
        p = Params(['target', '--key=value'])
        s = Statement('message', RESULT,
                      lambda x: Rule(x).has().option('key')
                                       .check().option_value_in_set('key', 'value')
                                       .empty().delimiters()
                                       .check().target(0, 'target'))

        self.assertEqual(s.attempt(p), RESULT)


if __name__ == '__main__':
    unittest.main()
