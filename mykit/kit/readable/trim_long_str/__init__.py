

## Birthdate: Oct 4, 2023
# def trim_long_str(input_str:str, /, max_char:int=100, nTab:int=3, make_it_raw:bool=True) -> str:
def trim_long_str(input_str:str, /, max_char:int=100, nTab:int=3) -> str:
    r"""
    Trim the `input_str` if its length is more than `max_char`

    ## Params
    - `input_str`: the input string. It's recommended to use `repr` if there are any
                    escaped characters to prevent them from being improperly truncated.
    - `max_char`: Let's say the string length is 100, but `max_char` is 35.
                    Then the remaining 65 characters (those in the middle of
                    the `input_str`) will be replaced by a placeholder "[X more chars]".
                    Note, even numbers are recommended.
    - `nTab`: the number of spaces before the placeholder (see examples below to learn more)

    ## Demo
    ```py
    x = 'super long string'
    print(trim_long_str(x))
    ```
    The output will look like this:
    ```txt
    aabbccddee...

       [2500 more chars]

    ...xxyyzz
    ```

    ## Demo II
    >>> print(trim_long_str(repr(SUPER_LONG_STR), nTab=os.get_terminal_size().columns//2))
    >>> aabbcc...
    >>>
    >>>                 [231 more chars]
    >>>
    >>> ...xx\nyyzz

    ## Docs
    - The reason why not using `os.get_terminal_size().columns//2` as the
        default `nTab` is because in a VM, it will raise an error since there is no terminal dimension.
    - There are minimal validations for function arguments. Please input appropriate values.
    - Also, using `nTab=os.get_terminal_size().columns//2` is a bit unreadable (makes it harder to find).  ~nicholas
    """

    str_len = len(input_str)

    ## Check
    if str_len <= max_char:
        return input_str
    
    ## Tweak: decrease max_char by 1 if it's an even number
    max_char = (max_char-1) if ( (max_char%2) != 0 ) else max_char

    remaining = str_len - max_char

    tab_str = ' '*nTab

    nHalf = int(max_char/2)

    return input_str[:nHalf] + f'...\n\n{tab_str}[{remaining} more chars]\n\n...' + input_str[-nHalf:]
