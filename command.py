from platform.params import makeParams, Params
from platform.exception import WrongOptions, WrongTargets


class Command:
    parent = None

    def __init__(self, parent):
        self.parent = parent

    def chain(self):
        ret = [self.name()]
        if self.parent is not None:
            ret = self.parent.chain() + ret
        return ret

    def path(self):
        return ' '.join(self.chain())

    def error(self, message):
        print(message)
        print('\n')
        print('-----------------------------------------------------')
        print('\n')
        self.__help()

    def needHelp(self, p: Params):
        return p.showHelp

    def execute(self, argv):
        try:
            p = makeParams(argv)

            if self.needHelp(p):
                self.__help()
            else:
                self.__check(p)
                self.__process(p)
        except WrongOptions as e:
            self.error(e)

        except WrongTargets as e:
            self.error(e)

        except Exception:
            raise

    def name(self):
        return 'Not implemented'

    def __help(self):
        pass

    def __check(self, p: Params):
        return False

    def __process(self, p: Params):
        pass

