from db.actions import Getter, Updater


class Database:
    def __init__(self, scheme):
        self._scheme = scheme
        scheme.check_and_create()

    def get(self):
        return Getter(self._scheme)

    def update(self):
        return Updater(self._scheme)
