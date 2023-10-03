import os as _os


def make_separator(char:str='─', /) -> str:
    r"""
    Equivalent to `char*_os.get_terminal_size()[0]`

    ## Demo
    >>> sep = make_separator('─')
    >>> print(sep + 'hi\n' + sep)
    """
    return char*_os.get_terminal_size()[0]
