from enum import Enum

class Color(Enum):
    black = 30
    red = 31
    green = 32
    yellow = 33
    blu= 34
    violent = 35
    cyan = 36
    white = 37

class Style(Enum):
    normal = 0
    bold = 1
    underline = 3

def start(c: Color, s: Style = Style.normal):
    return '\033[{style};{color}m'.format(style=s.value, color=c.value)

def end():
    return '\033[m'

def colored(str, color: Color, style: Style = Style.normal):
    return start(color, style) + str + end()