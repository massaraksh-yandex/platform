from subprocess import STDOUT, PIPE
from platform.execute.ssh import ssh


class run(object):
    def __init__(self, host = 'localhost', impl = ssh()):
        self._host = host
        self._args = []
        self._stderr = PIPE
        self._path = '.'
        self._impl = impl
        self.code = 0
        self.err = None
        self.out = ''

    def _collectdata(self, p):
        self.code = p.returncode
        self.out = p.communicate()[0].decode('utf-8')
        self.err = p.communicate()[1].decode('utf-8')

    def cmd(self, s):
        self._args = s
        return self

    def withstderr(self):
        self._stderr = STDOUT
        return self

    def path(self, p):
        self._path = p
        return self

    def call(self):
        p = self._impl.cmd(self._stderr, self._host, self._path, self._args)
        self._collectdata(p)
        return self.out

    def exec(self):
        p = self._impl.cmd(self._stderr, self._host, self._path, self._args)
        while True:
            line = p.stdout.readline().decode('utf-8')
            if line == '':
                break
            yield line

        self._collectdata(p)

