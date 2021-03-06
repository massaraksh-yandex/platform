import re
from platform.color.color import Color, Style, start, end, colored


class ColorRule:
    def __init__(self, regex, color: Color = Color.white, style: Style = Style.normal):
        self.regex = re.compile(regex)
        self.color = color
        self.style = style

    def apply(self, str):
        def transform(s, ind, c: Color, st: Style):
            first = s[:ind[0]] + start(c, st) + s[ind[0]:ind[1]]  + end()
            string = first + s[ind[1]:]
            return (string, len(first))

        i = 0
        while True:
            span = self.regex.search(str, i)
            if span is None:
                break
            ind = span.span()
            str, i = transform(str, ind, self.color, self.style)

        return str


class ReplaceRule:
    def __init__(self, regex, replace, color: Color = None, style: Style = Style.normal):
        self.regex = regex
        self.replace = colored(replace, color, style) if color is not None else replace

    def apply(self, str):
        return re.sub(self.regex, self.replace, str)


class Highlighter:
    def __init__(self, *rules):
        self.rules = rules

    def highlight(self, string):
        for rule in self.rules:
            string = rule.apply(string)
        return string


CR = ColorRule
RR = ReplaceRule