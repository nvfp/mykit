import math as _math


def byteFmt(__bytes: int, /) -> str:
    """in more readable byte format"""

    if __bytes == 0:
        return '0 B'

    exp = _math.floor(_math.log(abs(__bytes), 1024))
    val = round( __bytes / _math.pow(1024, exp), 2)

    UNIT = [
        'B', 'KiB', 'MiB',
        'GiB', 'TiB', 'PiB',
        'EiB', 'ZiB', 'YiB',
    ]

    return f'{val} {UNIT[exp]}'