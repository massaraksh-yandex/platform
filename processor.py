from queue import Queue, PriorityQueue
from threading import Thread


class Pipe:
    def __init__(self):
        self.input = Queue()
        self.output = Queue()
        self._opened = True
        self._index = 0

    def put(self, args):
        self.input.put( (self._index, args) )
        self._index += 1

    def closeAndWait(self):
        self._opened = False
        while self.input.qsize() or self.output.qsize():
            pass

    def _canProcess(self):
        return self.output.qsize() != 0 or self._opened

    def _getItem(self):
        r = self.input.get()
        self.input.task_done()
        return r

    def _prepare(self, args):
        self.output.put(args)

    def _getPrepared(self):
        r = self.output.get()
        self.output.task_done()
        return r

    def _canConsume(self):
        return self.output.qsize() != 0 or self._opened


class _Consumer:
    def __init__(self, f, pipe: Pipe):
        self.func = f
        self.pipe = pipe
        self.index = 0
        self.queue = []

    def __call__(self):
        from threading import active_count
        while self.pipe._canConsume():
            element = self.pipe._getPrepared()
            self.func(element[1])
            self.index += 1
            # if self.index == 500:
                # print ('active_count' + str(active_count()))
                # input()
            # self.queue.append(element)
            # self.queue.sort()
            # while len(self.queue) > 0 and self.queue[0][0] == self.index:
            #     el = self.queue.pop(0)
            #     self.func(el[1])
            #     self.index += 1


class _Worker:
    def __init__(self, f, pipe: Pipe):
        self.func = f
        self.pipe = pipe

    def __call__(self):
        while self.pipe._canProcess():
            item = self.pipe._getItem()
            self.pipe._prepare( (item[0], self.func(item[1])) )


def processor(map, consume, mapSize = 2):
    pipe = Pipe()
    for i in range(mapSize):
        t = Thread(target=_Worker(map, pipe))
        t.daemon = True
        t.start()

    t = Thread(target=_Consumer(consume, pipe))
    t.daemon = True
    t.start()

    return pipe

class Test:
    def __init__(self):
        from color import Highlighter, RR, Color, Style, CR
        self.hl = Highlighter(RR(r"\[with", '\n[\n with'), RR(r"\;", ';\n'),
                 CR(r"^[\/~][^\:]*", Color.cyan, Style.underline), CR(r"\serror\:", Color.red, Style.bold),
                 CR(r"\sОшибка", Color.red, Style.bold), CR(r"\swarning\:", Color.yellow),
                 RR(r",", ',', Color.green), RR(r"<", '<', Color.green),
                 RR(r">", '>', Color.green), CR(r"\[\s*\d+%\]", Color.violent))

        self.file = []
        with open('build.log') as f:
            self.file = f.readlines()

    def default_main(self):
        from subprocess import Popen, PIPE, STDOUT
        import sys
        proc = Popen('cat build.log', shell=True, stdout=PIPE, stderr=STDOUT, bufsize=0)
        path = '/home/massaraksh/workspace_2015-06-11'
        root = '~/ws'
        while True:
            line = proc.stdout.readline().decode("utf-8")
            if line == '':
                break

            line = line.replace(path, root)
            line = line.replace('/home', '/Users')
            line = self.hl.highlight(line)
            sys.stderr.write(line)
            sys.stderr.flush()
        proc.wait()

    def with_pipe(self):
        class Replacer:
            def __init__(self, path, root, highlighter, config):
                self.path = path
                self.root = root
                self.hl = highlighter
                self.cfg = config

            def __call__(self, line):
                line = line.replace(self.path, self.root)
                line = line.replace('/home', self.cfg)
                line = self.hl.highlight(line)
                return line

        def printLines(line):
            import sys
            sys.stderr.write(line)
            # sys.stderr.flush()

        from subprocess import Popen, PIPE, STDOUT
        repl = Replacer('/home/massaraksh/workspace_2015-06-11', '~/ws', self.hl, '/Users')
        pipe = processor(repl, printLines, 6)
        for line in self.file:
            pipe.put(line)
        # proc = Popen('cat build.log', shell=True, stdout=PIPE, stderr=STDOUT, bufsize=0)
        # while True:
            # line = proc.stdout.readline().decode("utf-8")
            # if line == '':
            #     break
            # pipe.put(line)
        pipe.closeAndWait()





    def simple(self):
        from subprocess import Popen, PIPE, STDOUT
        import sys
        proc = Popen('cat build.log', shell=True, stdout=PIPE, stderr=STDOUT, bufsize=0)
        while True:
            line = proc.stdout.readline().decode("utf-8")
            if line == '':
                break
            sys.stderr.write(line)
            sys.stderr.flush()
        proc.wait()


if __name__ == "__main__":
    # Test().simple()
    Test().with_pipe()
