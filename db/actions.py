import json


class Getter:
    def __init__(self, database):
        self.db = database

    def collection(self, obj_type):
        def func(element):
            with element as f:
                obj = obj_type.load_from(json.load(f))
                return obj.name, obj

        return dict(map(func, self.db.collection(obj_type)))

    def element(self, obj_type, name):
        with self.db.element(obj_type, name) as f:
            return obj_type.load_from(json.load(f))

    def object(self, name):
        obj_type = self.db.object_type(name)
        with self.db.object(name) as f:
            return obj_type.load_from(json.load(f))

    def config(self):
        with self.db.config() as f:
            return self.db.object_type('config').load_from(json.load(f))


class Updater:
    def __init__(self, database):
        self.db = database

    def collection(self, lst):

        getter = (lambda x: x) if isinstance(lst, list) else (lambda x: lst[x])

        for element in lst:
            self.element(getter(element))

    def element(self, obj):
        name = obj.name
        obj_type = type(obj)
        with self.db.element(obj_type, name, mode='w') as f:
            f.write(repr(obj))

    def object(self, obj):
        name = obj.name
        with self.db.object(name, mode='w') as f:
            f.write(repr(obj))

    def config(self, cfg):
        with self.db.config(mode='w') as f:
            f.write(repr(cfg))
