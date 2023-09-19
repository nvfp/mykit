from mykit.kit.color import colored_len as _colored_len


def paragraph_width(text:str, /) -> str:
    """
    Return the length of the longest line in the given multi-line text `text` (also works if `text` is a single line).
    This also works for colored text produced by the mykit `Colored` function.
    """
    k = 0
    for line in text.split('\n'):
        l = _colored_len(line)
        if l > k:
            k = l
    return k
