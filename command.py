from params import Params
from exception import WrongOptions
from exception import WrongTargets


class Command:
    def error(self, message):
        def printLine():
            print('-----------------------------------------------------')

        print(message)
        print('\n')
        printLine()
        print('\n')
        self.help()

    def needHelp(self, p):
        return len(p.options) == 1 and p.options[0] == 'help' and len(p.targets) == 0

    def execute(self, argv):
        try:
            p = Params(argv)

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
