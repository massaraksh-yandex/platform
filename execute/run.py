from subprocess import STDOUT, PIPE

from color.color import colored, Color
from execute.local import Local


class Run:
    def __init__(self, impl=Local()):
        self._args = []
        self._stderr = PIPE
        self._path = '.'
        self._impl = impl
        self.code = 0
        self.err = ''
        self.out = ''

    def _collect_data(self, p):
        res = p.communicate()
        self.out = res[0].decode('utf-8') if res[0] else ''
        self.err = res[1].decode('utf-8') if res[1] else ''
        self.code = p.returncode

    def cmd(self, s):
        self._args = s
        return self

    def join_err_and_out(self):
        self._stderr = STDOUT
        return self

    def path(self, p):
        self._path = p
        return self

    def call(self):
        p = self._impl.cmd(self._stderr, self._path, self._args)
        self._collect_data(p)
        return self.out

    def run(self):
        p = self._impl.cmd(self._stderr, self._path, self._args)
        self._collect_data(p)
        if self.code:
            raise Exception(colored(self.err, Color.red))
        return self

    def exec(self):
        p = self._impl.cmd(self._stderr, self._path, self._args)
        while True:
            line = p.stdout.readline().decode('utf-8')
            if line == '' and p.poll() is not None:
                break
            self.out += line
            yield line

        self.err = '\n'.join([l.decode('utf-8') for l in p.stderr.readlines()])
        self.code = p.returncode
