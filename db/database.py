from os.path import join, basename, splitext
from abc import ABCMeta, abstractmethod
from glob import glob
from os import remove
import json


class Database(metaclass=ABCMeta):
    def __init__(self, settings):
        self._settings = settings

    def _selectAll(self, path, type):
        ret = {}
        for name in glob(join(path, '*.json')):
            with open(name, 'r') as f:
                name = basename(splitext(name)[0])
                ret[name] = type(**json.load(f))
        return ret

    def _objPath(self, dir, name):
        return join(dir, name + '.json')

    @abstractmethod
    def _getDirByType(self, object):
        pass

    def update(self, object):
        path = self._getDirByType(object)

        with open(self._objPath(path, object.name), 'w') as f:
            f.write(repr(object))

    def remove(self, object):
        path = self._getDirByType(object)
        remove(join(path, object.name+'.json'))