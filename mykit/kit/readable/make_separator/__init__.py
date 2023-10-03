import os as _os
from typing import (
    Optional as _Optional
)


## birthdate: Oct 2, 2023
def make_separator(char:str='─', length:_Optional[int]=None) -> str:
    r"""
    Equivalent to `char*_os.get_terminal_size()[0]`

    ## Params
    - `char`: the separator character (should be a single char)
    - `length`: the separator length

    ## Demo
    >>> sep = make_separator('─')
    >>> print(sep + 'hi\n' + sep)
    """

    if length is None:
        try:
            L = _os.get_terminal_size().columns
        except OSError:  # OSError: [Errno 25] Inappropriate ioctl for device
            ## this exception is raised when calling this function inside a VM.
            ## i dont know why, but i guess it's because there's no "physical" terminal,
            ## so there's no sense of terminal dimensions. is this why this exception occurs?
            L = 21
    else:
        L = length

    return char*L
