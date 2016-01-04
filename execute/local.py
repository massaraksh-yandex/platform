from subprocess import Popen, PIPE


class Local(object):
    def cmd(self, error_stream, path, args):
        shell = not isinstance(args, list)
        command = 'cd {0} && {1}'.format(path, args) if shell else ['cd {0} && '.format(path)] + args
        return Popen(command, stdout=PIPE, stderr=error_stream, shell=shell, bufsize=0)
