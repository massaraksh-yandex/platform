import json
import unittest
import os
import os.path
from os.path import join
from db.scheme import SchemeFactory
from db.database import Database


class Square:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

    def __repr__(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def load_from(mmap):
        return Square(mmap['name'], mmap['x'], mmap['y'])


class Function:
    def __init__(self, name, attr):
        self.name = name
        self.attr = attr

    def __repr__(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def load_from(mmap):
        return Function(mmap['name'], mmap['attr'])


class Config:
    def __init__(self, name='config_name', attr='default_value'):
        self.name = name
        self.attr = attr

    def __repr__(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def load_from(mmap):
        return Config(mmap['name'], mmap['attr'])


def manually_create_scheme(path):
    os.mkdir(path)
    os.mkdir(join(path, 'collections'))
    os.mkdir(join(path, 'objects'))
    os.mkdir(join(path, 'collections', 'square'))

    with open(join(path, 'config.json'), 'w') as config:
        config.write('{ "name": "test_scheme", "attr": "test_attr" }')

    for arg in [('one', '1', '1'), ('two', '2', '4'), ('three', '3', '9')]:
        with open(join(path, 'collections', 'square', '{}.json').format(arg[0]), 'w') as file:
            file.write('{ "name": "%s", "x": "%s", "y": "%s" }'% arg)

    with open(join(path, 'objects', 'function.json'), 'w') as config:
        config.write('{ "name": "function", "attr": "square function" }')


def create_db():
    from tempfile import mkdtemp
    home = mkdtemp()
    manually_create_scheme(join(home, '.test_db'))
    scheme = SchemeFactory('test_db', Config, home).add_folder('square', Square)\
                                                   .add_object('function', Function)\
                                                   .product()

    return Database(scheme)


class TestGetter(unittest.TestCase):
    def setUp(self):
        self.db = create_db()

    def test_get_object(self):
        o = self.db.get().object('function')
        self.assertEqual(o.name, 'function')
        self.assertEqual(o.attr, 'square function')

    def test_get_element(self):
        one = self.db.get().element(Square, 'one')
        self.assertEqual(one.x, '1')
        self.assertEqual(one.y, '1')

        two = self.db.get().element(Square, 'two')
        self.assertEqual(two.x, '2')
        self.assertEqual(two.y, '4')

        three = self.db.get().element(Square, 'three')
        self.assertEqual(three.x, '3')
        self.assertEqual(three.y, '9')

    def test_get_collection(self):
        col = self.db.get().collection(Square)

        self.assertEqual(len(col), 3)
        for el in [('one', '1', '1'), ('two', '2', '4'), ('three', '3', '9')]:
            self.assertTrue(el[0] in col)
            self.assertEqual(el[1], col[el[0]].x)
            self.assertEqual(el[2], col[el[0]].y)

    def test_get_config(self):
        cfg = self.db.get().config()

        self.assertEqual(cfg.name, 'test_scheme')
        self.assertEqual(cfg.attr, 'test_attr')


class TestUpdater(unittest.TestCase):
    def setUp(self):
        self.db = create_db()

    def test_update_object(self):
        o = self.db.get().object('function')
        o.attr = 'линейная'
        self.db.update().object(o)
        res = self.db.get().object('function')

        self.assertEqual(res.attr, 'линейная')

    def test_update_element(self):
        o = self.db.get().element(Square, 'one')
        o.x = '4'
        o.y = '16'
        self.db.update().element(o)
        res = self.db.get().element(Square, 'one')

        self.assertEqual(res.x, '4')
        self.assertEqual(res.y, '16')

    def test_update_collection(self):
        col = self.db.get().collection(Square)

        self.assertEqual(len(col), 3)
        for el in [('one', '4', '16'), ('two', '5', '15'), ('three', '6', '36')]:
            o = col[el[0]]
            o.x = el[1]
            o.y = el[2]
        self.db.update().collection(col)

        res = self.db.get().collection(Square)

        self.assertEqual(len(res), 3)
        for el in [('one', '4', '16'), ('two', '5', '15'), ('three', '6', '36')]:
            self.assertTrue(el[0] in res)
            self.assertEqual(el[1], res[el[0]].x)
            self.assertEqual(el[2], res[el[0]].y)

    def test_update_config(self):
        new_attr = 'test_attr_2'
        cfg = self.db.get().config()
        cfg.attr = new_attr

        self.db.update().config(cfg)
        new_cfg = self.db.get().config()
        new_cfg.attr = new_attr

        self.assertEqual(new_cfg.name, 'test_scheme')
        self.assertEqual(new_cfg.attr, new_attr)

    def test_create_element(self):
        ten = Square('ten', '10', '100')

        old_col = self.db.get().collection(Square)
        old_col.update({'ten': ten})

        self.db.update().element(ten)
        new_col = self.db.get().collection(Square)

        self.assertEqual(len(old_col), len(new_col))
        for name in old_col:
            self.assertTrue(name in old_col)
            self.assertTrue(name in new_col)
            old_el = old_col[name]
            new_el = new_col[name]
            self.assertEqual(old_el.x, new_el.x)
            self.assertEqual(old_el.y, new_el.y)


if __name__ == '__main__':
    unittest.main()
