import unittest
from execute.run import Run
from execute.local import Local
from execute.ssh import Ssh


class TestRun(unittest.TestCase):
    def setUp(self):
        self.cases = [{
            'cmd': 'echo "output"',
            'code': '0',
            'out': 'output\n',
            'err': '',
            'need_join': False
        }, {
            'cmd': 'echo "output" 1>&2',
            'code': '0',
            'out': '',
            'err': 'output\n',
            'need_join': False
        }, {
            'cmd': 'echo "output" 1>&2',
            'code': '0',
            'out': 'output\n',
            'err': '',
            'need_join': True
        }]

    def test_local(self):
        for case in self.cases:
            p = Run(impl=Local()).cmd(case['cmd'])
            if case['need_join']:
                p.join_err_and_out()

            p.call()
            self.assertEqual(p.out, case['out'])
            self.assertEqual(p.err, case['err'])

    def test_ssh(self):
        for case in self.cases:
            p = Run(Ssh('localhost')).cmd(case['cmd'])
            if case['need_join']:
                p.join_err_and_out()

            p.call()
            self.assertEqual(p.out, case['out'])
            self.assertEqual(p.err, case['err'])

    def test_with_path(self):
        p = Run().path('/home').cmd(['pwd'])
        p.call()
        self.assertEqual(p.out, '/home\n')
        self.assertEqual(p.err, '')

    def test_with_sleep(self):
        p = Run().path('/home').cmd(['pwd', '&&', 'sleep', '1', '&&', 'pwd', ';', 'ls', '/asdf'])
        for line in p.exec():
            self.assertEqual(line, '/home\n')

        self.assertEqual(p.out, '/home\n/home\n')
        self.assertEqual(p.err, 'ls: /asdf: No such file or directory\n')
        self.assertEqual(p.code, 1)

