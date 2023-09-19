from mykit.kit.color import colored_len as _colored_len
from mykit.kit.readable.paragraph_width import paragraph_width as _paragraph_width


def box(text:str, /) -> str:
    """
    Surround the single/multi-line text `text` with a box.
    This also works for colored text produced by the mykit `Colored` function.

    ## Demo
    >>> box('test 123')
    >>> # ============
    >>> # ||test 123||
    >>> # ============
    """
    w = _paragraph_width(text)
    text_modified = ''
    for line in text.split('\n'):
        text_modified += '||' + line + ' '*(w-_colored_len(line)) + '||\n'
    return '='*(w+4) + '\n' + text_modified + '='*(w+4)
