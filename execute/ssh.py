from subprocess import Popen, PIPE


class Ssh(object):
    def __init__(self, host):
        self._host = host

    def _form_params(self, as_shell, path, args):
        if as_shell:
            return "ssh -T {0} 'cd {1} && {2}'".format(self._host, path, args)
        else:
            return ['ssh', '-T', self._host, 'cd {0} && '.format(path)] + args

    def cmd(self, error_stream, path, args):
        shell = not isinstance(args, list)
        c = self._form_params(shell, path, args)
        return Popen(c, stdout=PIPE, stderr=error_stream, shell=shell, bufsize=0)
