from platform.params import makeParams
from platform.exception import WrongOptions, WrongTargets


class Command:
    def error(self, message):
        print(message)
        print('\n')
        print('-----------------------------------------------------')
        print('\n')
        self.help()

    def needHelp(self, p):
        return len(p.options) == 1 and \
               p.options[0] == 'help' and \
               len(p.targets) == 0

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