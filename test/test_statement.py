import unittest
from statement.statement import Statement, InfoStatement
from statement.create import create
from statement.rule import Rule, Op, Data
from params.params import Params
from params.delimiter import SingleDelimiter, DoubleDelimiter
from params.exception import PlatformException


RESULT = 42


class TestOp(unittest.TestCase):
    def test_eq(self):
        self.assertTrue(Op.eq(1)(1))
        self.assertTrue(Op.eq(1.0)(1.0))
        self.assertTrue(Op.eq('1')('1'))
        self.assertTrue(Op.eq([1])([1]))

        self.assertFalse(Op.eq(1)(2))
        self.assertFalse(Op.eq(1.0)(2.0))
        self.assertFalse(Op.eq('1')('2'))
        self.assertFalse(Op.eq([1])([2]))

    def test_not_eq(self):
        self.assertFalse(Op.not_eq(1)(1))
        self.assertFalse(Op.not_eq(1.0)(1.0))
        self.assertFalse(Op.not_eq('1')('1'))
        self.assertFalse(Op.not_eq([1])([1]))

        self.assertTrue(Op.not_eq(1)(2))
        self.assertTrue(Op.not_eq(1.0)(2.0))
        self.assertTrue(Op.not_eq('1')('2'))
        self.assertTrue(Op.not_eq([1])([2]))

    def test_more(self):
        self.assertTrue(Op.more(1)(2))
        self.assertTrue(Op.more(1.0)(1.1))
        self.assertTrue(Op.more('1')('2'))
        self.assertTrue(Op.more([1])([2]))

        self.assertFalse(Op.more(1)(-1))
        self.assertFalse(Op.more(1.0)(0.9))
        self.assertFalse(Op.more('1')('0'))
        self.assertFalse(Op.more([1])([0]))

        self.assertTrue(Op.more(1, maybe_eq=True)(1))
        self.assertTrue(Op.more(1.0, maybe_eq=True)(1.0))
        self.assertTrue(Op.more('1', maybe_eq=True)('2'))
        self.assertTrue(Op.more([1], maybe_eq=True)([1]))

    def test_less(self):
        self.assertTrue(Op.less(1)(-1))
        self.assertTrue(Op.less(1.0)(0.9))
        self.assertTrue(Op.less('1')('0'))
        self.assertTrue(Op.less([1])([0]))

        self.assertFalse(Op.less(1)(2))
        self.assertFalse(Op.less(1.0)(1.1))
        self.assertFalse(Op.less('1')('2'))
        self.assertFalse(Op.less([1])([2]))

        self.assertTrue(Op.less(1, maybe_eq=True)(0))
        self.assertTrue(Op.less(1.0, maybe_eq=True)(0.0))
        self.assertTrue(Op.less('1', maybe_eq=True)('0'))
        self.assertTrue(Op.less([1], maybe_eq=True)([]))

    def test_expection_in_case_of_garbase_instead_of_the_data_enumeration(self):
        self.assertRaises(PlatformException, Rule._get_data, 'adf', Params([]))


class TestRule(unittest.TestCase):
    def setUp(self):
        self.p = Params(['target', '-', '--flag', '--key=value'])
        self.with_double_delimiter = Params(['target', '--', '--flag', '--key=value'])

    def test_delimiters_type(self):
        self.assertFalse(Rule().delimiter(DoubleDelimiter())(self.p))
        self.assertFalse(Rule().delimiter(SingleDelimiter())(self.with_double_delimiter))

        self.assertTrue(Rule().delimiter(SingleDelimiter())(self.p))
        self.assertTrue(Rule().delimiter(DoubleDelimiter())(self.with_double_delimiter))

    def test_delimiters_position(self):
        self.assertFalse(Rule().delimiter(DoubleDelimiter(2))(self.p))
        self.assertFalse(Rule().delimiter(SingleDelimiter(2))(self.with_double_delimiter))

        self.assertTrue(Rule().delimiter(SingleDelimiter(1))(self.p))
        self.assertTrue(Rule().delimiter(DoubleDelimiter(1))(self.with_double_delimiter))

    def test_target(self):
        self.assertTrue(Rule().target('target', 0)(self.p))

        self.assertFalse(Rule().target('target_wrong', 0)(self.p))
        self.assertFalse(Rule().target('target', 1)(self.p))

    def test_option(self):
        self.assertTrue(Rule().option('flag')(self.p))
        self.assertTrue(Rule().option('key', 'value')(self.p))
        self.assertTrue(Rule().option('key', 'value', 'value2')(self.p))

        self.assertFalse(Rule().option('flag', 'some_value')(self.p))
        self.assertFalse(Rule().option('key', 'value2')(self.p))
        self.assertFalse(Rule().option('key1')(self.p))

    def test_size(self):
        self.assertTrue(Rule().size(Data.Target, Op.eq(1))(self.p))
        self.assertTrue(Rule().size(Data.Delimiter, Op.eq(1))(self.p))
        self.assertTrue(Rule().size(Data.Option, Op.eq(2))(self.p))

        self.assertFalse(Rule().size(Data.Target, Op.eq(2))(self.p))
        self.assertFalse(Rule().size(Data.Delimiter, Op.eq(2))(self.p))
        self.assertFalse(Rule().size(Data.Option, Op.eq(1))(self.p))

    def test_empty(self):
        self.assertTrue(Rule().empty(Data.Target)(Params([])))
        self.assertTrue(Rule().empty(Data.Delimiter)(Params([])))
        self.assertTrue(Rule().empty(Data.Option)(Params([])))

        self.assertFalse(Rule().empty(Data.Target)(self.p))
        self.assertFalse(Rule().empty(Data.Delimiter)(self.p))
        self.assertFalse(Rule().empty(Data.Option)(self.p))

    def test_not_empty(self):
        self.assertFalse(Rule().not_empty(Data.Target)(Params([])))
        self.assertFalse(Rule().not_empty(Data.Delimiter)(Params([])))
        self.assertFalse(Rule().not_empty(Data.Option)(Params([])))

        self.assertTrue(Rule().not_empty(Data.Target)(self.p))
        self.assertTrue(Rule().not_empty(Data.Delimiter)(self.p))
        self.assertTrue(Rule().not_empty(Data.Option)(self.p))

    def test_has(self):
        self.assertTrue(Rule().has(Data.Target, 'target')(self.p))
        self.assertTrue(Rule().has(Data.Delimiter, SingleDelimiter())(self.p))
        self.assertTrue(Rule().has(Data.Option, 'key')(self.p))

        self.assertFalse(Rule().has(Data.Target, 'target1')(self.p))
        self.assertFalse(Rule().has(Data.Delimiter, DoubleDelimiter())(self.p))
        self.assertFalse(Rule().has(Data.Option, 'missing_key')(self.p))


class TestStatement(unittest.TestCase):
    def test_info_statement(self):
        self.assertEqual(None, InfoStatement('message').attempt(Params([])))
        self.assertEqual(None, InfoStatement('message').attempt(Params(['target', '--flga', '--'])))

    def test_empty_command(self):
        create('message').empty_command(RESULT)[0].attempt(Params([]))
        self.assertEqual(None, create('message').empty_command(RESULT)[0].attempt(Params(['target'])))
        self.assertEqual(None, create('message').empty_command(RESULT)[0].attempt(Params(['--flag'])))
        self.assertEqual(None, create('message').empty_command(RESULT)[0].attempt(Params(['--'])))

    def test_single_option_command(self):
        create('message').single_option_command(RESULT)[0].attempt(Params(['target']))
        self.assertEqual(None, create('message').single_option_command(RESULT)[0].attempt(Params([])))
        self.assertEqual(None, create('message').single_option_command(RESULT)[0].attempt(Params(['--'])))
        self.assertEqual(None, create('message').single_option_command(RESULT)[0].attempt(Params(['--flag'])))

    def test_complex1(self):
        p = Params(['target', '--', '--flag', '--key=value'])
        s = Statement('message', RESULT,
                      rule=Rule().delimiter(DoubleDelimiter())
                                 .option('flag')
                                 .option('key', 'value')
                                 .target('target', 0))

        self.assertEqual(s.attempt(p), RESULT)

    def test_complex2(self):
        p = Params(['target', '--key=value'])
        s = Statement('message', RESULT,
                      Rule().option('key', 'value')
                            .empty(Data.Delimiter)
                            .target('target', 0))

        self.assertEqual(s.attempt(p), RESULT)
