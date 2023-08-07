import math as _math
import re as _re
from typing import (
    NoReturn as _NoReturn,
    Union as _Union
)


def connum(num: _Union[str, int, float], /) -> _Union[str, _NoReturn]:
    """
    connum (Concise Number).
    Displaying the number as is, without plus signs or extra zeroes, for the UI.

    ---

    ## Exceptions
    - `ValueError` if `num` is not a number-like

    ## Demo
    - `connum(3.0)` -> `'3'`
    - `connum('+03.500')` -> `'3.5'`
    """
    res = _re.match(r'^(?P<sign>\+|-)?[0]*(?P<int>\d+)(?:(?P<dec>\.\d*?)[0]*)?$', str(num))
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

def in_byte(bytes: int, /, precision: int = 2, gap: int = 1) -> str:
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
    - `in_byte` is the extended version of `mykit.kit.text.byteFmt`
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
    power = _math.floor( _math.log(bytes, 1024) )

    number = round( bytes / _math.pow(1024, power), precision )

    UNIT = [
        'B', 'KiB', 'MiB',
        'GiB', 'TiB', 'PiB',
        'EiB', 'ZiB', 'YiB',
    ]

    return sign + connum(number) + GAP + UNIT[power]


def num_approx(num:float, /, precision:int=1, gap:int=0) -> str:
    """
    Round a number down to K (thousand), M (million), B (billion), etc.

    ---

    ## Params
    - `precision`: rounding precision
    - `gap`: gap (in spaces) between the number and the unit

    ## Demo
    >>> num_approx(999)  # 999
    >>> num_approx(1000)  # 1K
    >>> num_approx(1001)  # 1K
    >>> num_approx(1_250_000)  # 1.2M
    >>> num_approx(1_250_000, 0, 1)  # 1 M
    >>> num_approx(1_750_000, 0, 1)  # 2 M
    """

    suffixes = [
        (1e3, ''),
        (1e6, 'K'),
        (1e9, 'M'),
        (1e12, 'B'),
        (1e15, 'T'),
        (1e18, 'q'),  # quadrillion
        (1e21, 'Q'),  # Quintillion
        (1e24, 's'),  # sextillion
        (1e27, 'S'),  # Septillion
    ]

    ## Handle negative `num`
    sign = ''
    if num < 0:
        num = abs(num)
        sign = '-'

    for divisor, suffix in suffixes:
        if num < divisor:
            n_format = f'{num*1000/divisor:.{precision}f}'
            break

    ## Remove trailing zeros after the decimal point if precision is greater than 0
    if precision > 0:
        n_format = n_format.rstrip('0').rstrip('.')
    
    GAP = ''
    if suffix != '':
        GAP = ' '*gap

    return sign + n_format + GAP + suffix


def num_round(number:int, /, keep:int=2, add_commas:bool=True) -> str:
    """
    Rounding number (see demo below).

    ---
    
    ## Params
    - `number`: The input number; floats are also accepted.
    - `keep`: number of the non-zero part (see demo below)
    - `add_commas`: separated the thousands with commas

    ## Demo
    >>> num_round(12345, 1)  # 10,000
    >>> num_round(12345, 2)  # 12,000
    >>> num_round(12345, 3)  # 12,300
    >>> num_round(12385, 3)  # 12,400

    ## Docs
    - `keep` value is clamped to a minimum of 1.
    """

    ## Handle float
    number = round(number)

    ## Handle negative number
    sign = ''
    if number < 0:
        number = abs(number)
        sign = '-'

    ## Clamp
    keep = min(len(str(number)), max(1, keep))
    
    ## Rounding
    power = len(str(number)) - keep
    scale = int( _math.pow(10, power) )
    rounded = round(number/scale)*scale

    ## Stringify
    if add_commas:
        rounded = f'{rounded:,}'
    else:
        rounded = str(rounded)

    return sign + rounded