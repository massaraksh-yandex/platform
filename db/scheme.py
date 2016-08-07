import json
import os
from os.path import expanduser, join
from params.exception import PlatformException


class Scheme:
    def __init__(self, name, collections, objects, home):
        self._objects = objects
        self._collections = collections
        self._path = join(home, '.'+name)
        self._object_prefix = join(self._path, 'objects')
        self._collection_prefix = join(self._path, 'collections')

    def _object_path(self, name):
        prefix = self._path if name == 'config' else self._object_prefix
        return join(prefix, name+'.json')

    def _collection_path(self, col_type, element=None):
        name = self._collections[col_type]

        if element:
            if len(element) <= 5 or element[-5:] != '.json':
                element_name = element+'.json'
            else:
                element_name = element
        else:
            element_name = ''

        return join(self._collection_prefix, name, element_name)

    def collection(self, obj_type, mode='r'):
        def func(element):
            return open(self._collection_path(obj_type, element), mode)

        if obj_type not in self._collections:
            raise Exception('Cannot find collection with type "{}"'.format(obj_type))

        path = self._collection_path(obj_type)
        return list(map(func, os.listdir(path)))

    def element(self, obj_type, name, mode='r'):
        if obj_type not in self._collections:
            raise Exception('Cannot find collection with type "{}"'.format(obj_type))

        return open(self._collection_path(obj_type, name), mode)

    def object(self, name, mode='r'):
        if name not in self._objects:
            raise Exception('Cannot find object with name "{}"'.format(name))

        path = self._object_path(name)
        return open(path, mode)

    def config(self):
        if 'config' not in self._objects:
            raise Exception('Cannot find config object')

        path = self._object_path('config')

        with open(path) as f:
            return self._objects['config'].load_from(json.load(f))

    def set_config(self, cfg):
        if 'config' not in self._objects:
            raise Exception('Cannot find config object')

        path = self._object_path('config')

        with open(path, 'w') as f:
            f.write(repr(cfg))

    def object_type(self, name):
        return self._objects[name]

    def check_and_create(self):
        folders = [self._collection_path(c) for c in self._collections] + \
                  [self._collection_prefix, self._object_prefix, self._path]

        for f in folders:
            if not os.path.exists(f):
                os.makedirs(f, exist_ok=True)
            elif not os.path.isdir(f):
                raise Exception('Object "{}" must be a folder'.format(f))

        for o in [join(self._object_path(ob)) for ob in self._objects]:
            if not os.path.exists(o):
                if not os.path.isfile(o):
                    raise Exception('Object "{}" must be a file'.format(o))
                with self.object(o) as f:
                    json.dump(self._objects[0](), f)


class Fake:
    def __init__(self, config_type):
        self._config_type = config_type

    def collection(self, obj_type, mode='r'):
        raise PlatformException('method is not implemented in fake scheme')

    def element(self, obj_type, name, mode='r'):
        raise PlatformException('method is not implemented in fake scheme')

    def object(self, name, mode='r'):
        raise PlatformException('method is not implemented in fake scheme')

    def object_type(self, name):
        raise PlatformException('method is not implemented in fake scheme')

    def check_and_create(self):
        pass

    def config(self):
        return self._config_type()

    def set_config(self, cfg):
        raise PlatformException('method is not implemented in fake scheme')


class SchemeFactory:
    def __init__(self, name, configuration_type, home=expanduser('~')):
        self._name = name
        self._collections = {}
        self._objects = {'config': configuration_type}
        self._home = home

    def add_folder(self, name, obj_type):
        self._collections.update({obj_type: name})
        return self

    def add_object(self, name, obj_type):
        self._objects.update({name: obj_type})
        return self

    def product(self, fake=False):
        if fake:
            return Fake(self._objects['config'])
        else:
            return Scheme(self._name, self._collections, self._objects, self._home)
