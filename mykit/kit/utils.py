import datetime as _datetime
import keyword as _keyword
import os as _os
import random as _random
import time as _time
from typing import (
    Dict as _Dict,
    Hashable as _Hashable,
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
    >>> printer('INFO: foo')     # [06:15:09] INFO: foo
    >>> printer('WARNING: bar')  # [06:15:09] WARNING: bar
    """
    T = _datetime.datetime.now().strftime('%H:%M:%S')
    print(f'[{T}] {__msg}')

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
    printer(__msg)

def print_screen(__msg: str, /) -> None:
    """prints message at the bottom of the terminal screen, adapting to terminal's height."""

    ## the height of users' terminal
    h = _os.get_terminal_size()[1]

    ## message height
    n = len( __msg.split('\n') )
    
    print( '\n'*(h-n) + __msg )


def sort_dict_by_key(input_dict:dict, /, reverse:bool=False) -> dict:
    """Sort dictionary by keys (keys should be sortable).

    ---
    
    ## Demo
    >>> sort_dict_by_key({'b': 3, 'a': 1, 'c': 2}, 0)  # {'a': 1, 'b': 3, 'c': 2}
    >>> sort_dict_by_key({'b': 3, 'a': 1, 'c': 2}, 1)  # {'c': 2, 'b': 3, 'a': 1}
    >>> sort_dict_by_key({3: 0, 1: 0, 2: 0}, 0)  # {1: 0, 2: 0, 3: 0}
    >>> sort_dict_by_key({3: 0, 1: 0, 2: 0}, 1)  # {3: 0, 2: 0, 1: 0}
    """
    out = {
        k: input_dict[k]
        for k in sorted(input_dict, reverse=reverse)
    }
    return out

def sort_dict_by_val(input_dict:dict, /, reverse:bool=False) -> dict:
    """Sort dictionary by values (values should be sortable).

    ---
    
    ## Demo
    >>> sort_dict_by_val({'x': 'b', 'y': 'a', 'z': 'c'}, 0)  # {'y': 'a', 'x': 'b', 'z': 'c'}
    >>> sort_dict_by_val({'x': 'b', 'y': 'a', 'z': 'c'}, 1)  # {'z': 'c', 'x': 'b', 'y': 'a'}
    >>> sort_dict_by_val({'a': 3, 'b': 1, 'c': 2}, 0)  # {'b': 1, 'c': 2, 'a': 3}
    >>> sort_dict_by_val({'a': 3, 'b': 1, 'c': 2}, 1)  # {'a': 3, 'c': 2, 'b': 1}
    """
    out = {
        k: input_dict[k]
        for k in sorted(input_dict, key=input_dict.get, reverse=reverse)
    }
    return out


def get_first_n_dict_items(input_dict:dict, /, first_n:int) -> dict:
    """
    Get the first `first_n` items from the dictionary.

    ---

    ## Params
    - `first_n`: should be at least 0. If it's negative, it'll be set to 0.
    """
    out = {
        k: input_dict[k]
        for k in list(input_dict)[:max(0, first_n)]
    }
    return out

def get_last_n_dict_items(input_dict:dict, /, last_n:int) -> dict:
    """
    Get the last `last_n` items from the dictionary.

    ---

    ## Params
    - `last_n`: should be at least 0. If it's negative, it'll be set to 0.
    """
    last_n = max(0, last_n)
    if last_n == 0: return {}
    return {
        k: input_dict[k]
        for k in list(input_dict)[-last_n:]
    }


def randhex(length:int=3, /) -> str:
    """
    Get a random hexadecimal string

    ---

    ## Demo
    >>> randhex()    # 13d
    >>> randhex()    # 3c4
    >>> randhex(7)   # f971445
    >>> randhex(21)  # 9aa4d78014ba3416dec3b
    """
    hex = '0123456789abcdef'
    return ''.join(_random.choices(hex, k=length))


def reverse_dict(input_dict: dict, /) -> dict:
    """
    Reverse the order of dict items

    ---

    ## Demo
    >>> reverse_dict({'a': 0, 'b': 0, 'c': 0})  # {'c': 0, 'b': 0, 'a': 0}
    >>> reverse_dict({5: '', 1: '', 9: ''})  # {9: '', 1: '', 5: ''}
    """
    keys = list(input_dict.keys())
    keys.reverse()
    return {
        k: input_dict[k]
        for k in keys
    }


def merge_dicts(
    dict1:_Dict[_Hashable, float],
    dict2:_Dict[_Hashable, float],
    /
) -> _Dict[_Hashable, float]:
    """
    Merge two dictionaries, returning the merged result,
    while keeping both input dictionaries `dict1` and `dict2` intact.

    ---

    ## Demo
    >>> dict1 = {'a': 1, 'b': 2}
    >>> dict2 = {'b': 3, 'c': 4}
    >>> merged_dict = merge_dicts(dict1, dict2)
    >>> # merged_dict is {'a': 1, 'b': 5, 'c': 4}

    ## Docs
    - See also `mykit.kit.utils.merging_dicts`
    """
    dict1 = dict1.copy()
    dict2 = dict2.copy()

    for key, value in dict2.items():
        if key in dict1:
            dict1[key] += value
        else:
            dict1[key] = value

    return dict1

def merging_dicts(
    dict1:_Dict[_Hashable, float],
    dict2:_Dict[_Hashable, float],
    /
) -> None:
    """
    Merge `dict2` into `dict1` (`dict2` unchanged).

    ---

    ## Demo
    >>> dict1 = {'a': 1, 'b': 2}
    >>> dict2 = {'b': 3, 'c': 4}
    >>> merging_dicts(dict1, dict2)
    >>> # dict1 will be {'a': 1, 'b': 5, 'c': 4}
    >>> # dict2 will be {'b': 3, 'c': 4}

    ## Docs
    - Also see `mykit.kit.utils.merge_dicts`
    """
    for key, value in dict2.items():
        if key in dict1:
            dict1[key] += value
        else:
            dict1[key] = value


def add_dict_val(
    the_dict:_Dict[_Hashable, float],
    key:_Hashable,
    add:float=1,
    init:float=1,
) -> None:
    """
    Add or initialize a value in the given dictionary

    ---

    ## Params
    - `the_dict`: A dictionary to which the value will be added or initialized.
    - `key`: The key for which the value will be modified or initialized.
    - `add`: The value to be added to the existing value associated with the key.
    - `init`: The initial value to set for the key if it doesn't exist.

    ## Demo
    >>> my_dict = {'apple': 5, 'banana': 3}
    >>> add_dict_val(my_dict, 'apple', 1, 1)
    >>> # After the function call, my_dict will be: {'apple': 6, 'banana': 3}
    >>> add_dict_val(my_dict, 'pear', 2, 0)
    >>> # After the function call, my_dict will be: {'apple': 6, 'banana': 3, 'pear': 0}
    """
    if key in the_dict:
        the_dict[key] += add
    else:
        the_dict[key] = init