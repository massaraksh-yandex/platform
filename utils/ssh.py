from subprocess import Popen, PIPE, STDOUT


class ssh(object):
    def __init__(self, host):
        self.host = host
        self.args = []
        self.shell = False
        self.stderr = None

    def _formparams(self):
        return 'ssh {0} {1}'.format(self.host, self.args) if self.shell else ['ssh', self.host] + self.args

    def _formcommand(self):
        return Popen(self._formparams(), stdout=PIPE, stderr=self.stderr, shell=self.shell, bufsize=0)

    def cmdstr(self, s):
        self.args = s
        self.shell = True
        return self

    def cmdargs(self, args):
        self.args = args
        return self

    def joinwithstderr(self):
        self.stderr = STDOUT
        return self

    def call(self):
        return self._formcommand().communicate()[0].decode('utf-8')

    def exec(self):
        p = self._formcommand()
        while True:
            line = p.stdout.readline().decode('utf-8')
            if line == '':
                break
            yield line