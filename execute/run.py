from subprocess import STDOUT, PIPE
from execute.ssh import Ssh


class Run(object):
    def __init__(self, impl=Ssh('localhost')):
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

    def exec(self):
        p = self._impl.cmd(self._stderr,self._path, self._args)
        while True:
            line = p.stdout.readline().decode('utf-8')
            if line == '' and p.poll() is not None:
                break
            yield line

        self._collect_data(p)
