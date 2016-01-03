class PlatformException(Exception):
    pass


class WrongOptions(PlatformException):
    pass


class WrongTargets(PlatformException):
    pass


class WrongDelimiters(PlatformException):
    pass