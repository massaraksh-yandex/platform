from enum import Enum
import re


class Color(Enum):
    black = 30
    red = 31
    green = 32
    yellow = 33
    blue= 34
    violent = 35
    cyan = 36
    white = 37

class Style(Enum):
    normal = 0
    bold = 1
    underline = 4


def start(c: Color, s: Style = Style.normal):
    return '\033[{style};{color}m'.format(style=s.value, color=c.value)


def end():
    return '\033[m'


def colored(str, color: Color, style: Style = Style.normal):
    return start(color, style) + str + end()


class ColorRule:
    def __init__(self, regex, color: Color = Color.white, style: Style = Style.normal):
        self.regex = re.compile(regex)
        self.color = color
        self.style = style

    def apply(self, str):
        def transform(s, ind, c: Color, st: Style):
            return s[:ind[0]] + start(c, st) + s[ind[0]:ind[1]]  + end() + s[ind[1]:]

        for s in self.regex.finditer(str):
            str = transform(str, s.span(), self.color, self.style)
            break
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