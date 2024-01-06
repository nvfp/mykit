import math
import re

def _connum(num):
    res = re.match(r'^(?P<sign>\+|-)?[0]*(?P<int>\d+)(?:(?P<dec>\.\d*?)[0]*)?$', str(num))
    if res is None:
        raise ValueError(f'Invalid numeric input: {repr(num)}.')

    sign, int, dec = res.groups()

    if sign in (None, '+'):
        ## Positive: omit the "+" sign (if any)
        out = ''
    else:
        if (int == '0') and (dec in (None, '.')):
            ## Handle "-0"
            out = ''
        else:
            out = '-'

    out += int

    if dec not in (None, '.'):
        ## Only if it's a decimal number (not like 123.0)
        out += dec

    return out

def fmt_byte(bytes:int, /, precision:int=2, gap:int=1) -> str:
    """
    ## Params
    - `precision`: rounding precision
    - `gap`: gap (in spaces) between the number and the unit

    ## Demo
    >>> in_byte(100)  # 100 B
    >>> in_byte(1300)  # 1.27 KiB
    >>> in_byte(1300, 0, 0)  # 1KiB
    >>> in_byte(1700, 0, 0)  # 2KiB

    ## Docs
    - is from `mykit.kit.text`
    """

    GAP = ' '*gap

    ## Handle 0 `bytes`
    if bytes == 0: return '0' + GAP + 'B'

    ## Handle float `bytes`
    bytes = round(bytes)

    ## Handle negative `bytes`
    sign = ''
    if bytes < 0:
        bytes = abs(bytes)
        sign = '-'

    ## Calculate the exponent of 1024
    power = math.floor( math.log(bytes, 1024) )

    number = round( bytes / math.pow(1024, power), precision )

    UNIT = [
        'B', 'KiB', 'MiB',
        'GiB', 'TiB', 'PiB',
        'EiB', 'ZiB', 'YiB',
    ]

    return sign + _connum(number) + GAP + UNIT[power]
