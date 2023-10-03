import os as _os
from typing import (
    Optional as _Optional
)


## birthdate: Oct 2, 2023
def make_separator(char:str='─', length:_Optional[int]=None, length_backup:int=21) -> str:
    r"""
    Equivalent to `char*_os.get_terminal_size()[0]`

    ## Params
    - `char`: the separator character (should be a single char)
    - `length`: the separator length
    - `length_backup`: Used with `length=None` when an `OSError` arises (check this function code for details)

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
            L = length_backup
    else:
        L = length

    return char*L
