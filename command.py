from platform.params import makeParams, Params
from platform.exception import WrongOptions, WrongTargets


class Command:
    def error(self, message):
        print(message)
        print('\n')
        print('-----------------------------------------------------')
        print('\n')
        self.help()

    def needHelp(self, p: Params):
        return p.showHelp

    def execute(self, argv):
        try:
            p = makeParams(argv)

            if self.needHelp(p):
                self.help()
            else:
                self.check(p)
                self.process(p)
        except WrongOptions as e:
            self.error(e)

        except WrongTargets as e:
            self.error(e)

        except Exception:
            raise