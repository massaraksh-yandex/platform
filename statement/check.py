from params.exception import WrongDelimiters, WrongOptions, WrongTargets


class Check:
    def __init__(self, rule):
        self.rule = rule
        self.p = rule.params

    def delimiters_type(self, obj_type):
        for d in self.p.delimiters:
            if not isinstance(d, obj_type):
                raise WrongDelimiters()
        return self.rule

    def option_names_in_set(self, *lst):
        for o in self.p.options:
            if o not in lst:
                raise WrongOptions()
        return self.rule

    def option_value_in_set(self, name, *lst):
        value = self.p.options[name]
        if not value and None not in lst:
            raise WrongOptions()
        if value not in lst:
            raise WrongOptions()
        return self.rule

    def target(self, index, pattern):
        if self.p.targets[index].value != pattern:
            raise WrongTargets()
        return self.rule
