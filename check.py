from platform.exception import WrongDelimers, WrongOptions, WrongTargets
from platform.params import Params


class Size:
    @staticmethod
    def equals(arr, size, message = None):
        if len(arr) != size:
            m = 'Неверный размер массива: ожидалось {0}, получен {1}'.format(len(arr), size)
            raise ValueError(m if not message else message)
        return True

    @staticmethod
    def moreOrEquals(arr, size, message = None):
        if len(arr) < size:
            m = 'Неверный размер массива: ожидалось как минимум {0}, получен {1}'.format(len(arr), size)
            raise ValueError(m if not message else message)
        return True

    @staticmethod
    def notEquals(arr, size, message = None):
        if len(arr) == size:
            m = 'Неверный размер массива: ожидалось {0}, получен {1}'.format(len(arr), size)
            raise ValueError(m if not message else message)
        return True

    @staticmethod
    def bounds(arr, low, high, message = None):
        if low <= len(arr) < high:
            m = 'Неверный размер массива: ожидалось {0} < {1} < {2}'.format(low, len(arr), high)
            raise ValueError(m if not message else message)
        return True


class Check:
    @staticmethod
    def delimerType(delimer, type):
        if not isinstance(delimer, type):
            raise WrongDelimers('Неверный тип разделителя: получен {0}, ожидался {1}'
                                .format(delimer.__name__, type.__name__))
        return True

    @staticmethod
    def optionNamesInSet(p: Params, set):
        for o in p.options:
            if o not in set:
                raise WrongOptions('Опция {0} отсутствует в списке разрешённых: {1}'.format(o, str(p.options)))
        return True


class Empty:
    @staticmethod
    def options(p: Params):
        if p.options:
            raise WrongOptions('Опции должны быть пусты: {0}'.format(str(p.options)))
        return True

    @staticmethod
    def array(arr):
        if arr:
            raise ValueError('Массив должен быть пуст: {0}'.format(str(arr)))
        return True

    @staticmethod
    def delimers(p: Params):
        if p.delimer:
            raise WrongDelimers('Разделители должны быть пусты: {0}'.format(str(p.delimer)))
        return True

    @staticmethod
    def targets(p: Params):
        if p.targets:
            raise WrongTargets('Цели должны быть пусты: {0}'.format(str(p.targets)))
        return True


class NotEmpty:
    @staticmethod
    def options(p: Params):
        if not p.options:
            raise WrongOptions('Опции должны быть не пусты')
        return True

    @staticmethod
    def array(arr):
        if not arr:
            raise ValueError('Массив должен быть не пуст')
        return True

    @staticmethod
    def delimers(p: Params):
        if not p.delimer:
            raise WrongDelimers('Разделители должны быть не пусты')
        return True

    @staticmethod
    def targets(p: Params):
        if not p.targets:
            raise WrongTargets('Цели должны быть не пусты')
        return True

class Has:
    @staticmethod
    def option(p: Params, option):
        if option not in p.options:
            raise WrongOptions('Ожидалась опция {0}, однако получено {1}'.format(option, str(p.options)))
        return True

    @staticmethod
    def inArray(arr, el, message = None):
        if el not in arr:
            m = 'Отсутсвует элемент {0}, получено {1}'.format(el, str(arr))
            raise ValueError(m if message is None else message)
        return True

def emptyCommand(func):
    return [lambda p: func if Empty.delimers(p) and
                              Empty.options(p) and
                              Empty.targets(p)
                       else raiseWrongParsing()]


def singleOptionCommand(res, functor = lambda p: True):
    return [lambda p: res if Empty.delimers(p) and
                             Empty.options(p) and
                             Size.equals(p.targets, 1) and
                             functor(p)
                      else raiseWrongParsing()]


def raiseWrongParsing():
    raise ValueError('Ошибочное условие')

def recieverOptions(map):
    return [lambda p: p.argv[0] if Has.inArray(map, p.argv[0]) else raiseWrongParsing()]

