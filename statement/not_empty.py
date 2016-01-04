from params.exception import WrongOptions, PlatformException, WrongDelimiters, WrongTargets


class NotEmpty:
    def __init__(self, rule):
        self.rule = rule
        self.p = rule.params

    def options(self):
        if not self.p.options:
            raise WrongOptions('Опции должны быть не пусты')
        return self.rule

    def array(self, arr):
        if not arr:
            raise PlatformException('Массив должен быть не пуст')
        return self.rule

    def delimiters(self):
        if not self.p.delimiters:
            raise WrongDelimiters('Разделители должны быть не пусты')
        return self.rule

    def targets(self):
        if not self.p.targets:
            raise WrongTargets('Цели должны быть не пусты')
        return self.rule
