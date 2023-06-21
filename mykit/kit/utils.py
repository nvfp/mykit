import datetime as _datetime
import keyword as _keyword
import os as _os
import random as _random
import time as _time
from typing import (
    Tuple as _Tuple
)


def randfloat(__low: float, __high: float, __prec: int = 2, /) -> float:
    """
    This function follows `random.uniform` behaviors.
    `__prec`: float precision (>= 0); if `__low` at 2 decimal point (`0.25`), `__prec` should at least `2`.
    `__prec` normally max at 15-18 (depends on system).
    """

    ## can't use below because each end only half probability-dense
    # return round(_random.uniform(__low, __high), __prec)

    k = pow(10, __prec)
    return _random.randint(round(__low*k), round(__high*k)) / k


def randrange(low: float, high: float, len: float, /, pad: float = 0.1, prec: int = 3) -> _Tuple[float, float]:
    """
    if `low = 0, high = 1` -> include both `0` and `1`.
    if `low = 0, high = 1, pad = 0.1` -> include both `0.1` and `0.9`.

    `pad`: should `0 <= pad < 0.5`
    """

    range_len = high - low
    the_pad = range_len * pad

    start = randfloat(low + the_pad, high - the_pad - len, prec)
    end = start + len

    return (start, end)


def minmax_normalization(x: float, min: float, max: float, /) -> float:
    """min-max feature scaling"""
    return (x - min) / (max - min)


def slice_list(__in: list, __n: int, /) -> list:
    """if `__n = 2` -> `[1, 2, 3, 4, 5]` -> `[[1, 2], [3, 4], [5]]`"""
    out = [
        __in[i : i + __n]
        for i in range(0, len(__in), __n)
    ]
    return out


def map_range(__value, /, from_min, from_max, to_min, to_max) -> float:
    """
    Maps a value from one range to another.

    ---

    ## Params
        - `__value`: The value to be mapped
        - `from_min`: The minimum value of the original range
        - `from_max`: The maximum value of the original range
        - `to_min`: The minimum value of the target range
        - `to_max`: The maximum value of the target range

    ## Returns
        - The mapped value in the target range.

    ## Demo
        >>> original_value = 5
        >>> mapped_value = map_range(original_value, 1, 9, 0, 1)
        >>> print(mapped_value)
        0.5
    """
    
    ## normalize the value from the original range
    normalized_value = (__value - from_min) / (from_max - from_min)

    ## scale the normalized value to the target range
    mapped_value = normalized_value * (to_max - to_min) + to_min

    return mapped_value


def is_valid_var_name(__in: str, /) -> bool:
    """
    Check if a string `__in` is valid for variable name.

    ---

    ## Demo
    - `is_valid_var_name('2x')` -> `False`
    - `is_valid_var_name('x2')` -> `True`
    - `is_valid_var_name('cold-ice')` -> `False`
    - `is_valid_var_name('cold_ice')` -> `True`
    """
    return (__in.isidentifier() and (not _keyword.iskeyword(__in)))


def printer(__msg: str, /) -> None:
    """
    For simple logging needs.
    
    ---

    ## Demo
    >>> printer('INFO: foo')  # [06:15:09] INFO: foo
    >>> printer('WARNING: bar')  # [06:15:09] WARNING: bar
    """
    print(f'[{_datetime.datetime.now().strftime("%H:%M:%S")}] {__msg}')

def slowprint(__msg: str, /, delay: float = 0.15) -> None:
    """
    For simple logging needs.
    Basically the same as `mykit.kit.utils.printer` but with delay.

    ---

    ## Params
    - `delay`: in seconds

    ## Demo
    >>> for i in range(3):
    >>>     slowprint(f'INFO: {i}')
    >>> ## output:
    >>> ## [06:38:32] INFO: 0
    >>> ## [06:38:32] INFO: 1
    >>> ## [06:38:33] INFO: 2
    """
    _time.sleep(delay)
    print(f'[{_datetime.datetime.now().strftime("%H:%M:%S")}] {__msg}')

def print_screen(__msg: str, /) -> None:
    """prints message at the bottom of the terminal screen, adapting to terminal's height."""

    ## the height of users' terminal
    h = _os.get_terminal_size()[1]

    ## message height
    n = len( __msg.split('\n') )
    
    print( '\n'*(h-n) + __msg )
