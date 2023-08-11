import os
from pathlib import Path as _Path


def _compare(dir, ref, cmp):
    """
    - `dir`: The current iterated directory
    - `ref`: Reference
    - `cmp`: Comparison
    """

    dir_rel = os.path.relpath(dir, ref)
    dir_cmp_pth = os.path.join(cmp, dir_rel)
    if not os.path.isdir(dir_cmp_pth): raise AssertionError('The current iterated directory is missing in the comparison.')

    for thing in os.listdir(dir):
        thing_pth = os.path.join(dir, thing)

        if os.path.isfile(thing_pth):
            file_rel = os.path.relpath(thing_pth, ref)
            file_cmp_pth = os.path.join(cmp, file_rel)
            if not os.path.isfile(file_cmp_pth): raise AssertionError('The current iterated file is missing in the comparison.')
            with open(thing_pth, 'r') as f: text1 = f.read()
            with open(file_cmp_pth, 'r') as f: text2 = f.read()
            if text1 != text2: raise AssertionError('File content differs between ref and cmp directories.')
        else:
            _compare(thing_pth, ref, cmp)


def equaldirs(dir1:_Path, dir2:_Path, /) -> bool:
    """
    Return `True` if `dir1` and `dir2` are equal (recursively; all the
    file and subdir names in both dirs are the same; all files have
    the same content; but note that file metadata (such as modified/created
    date) may not be considered). Return `False` otherwise.

    ---

    ## Params
    - `dir1`: Absolute path to the directory-1
    - `dir2`: Absolute path to the directory-2

    ## Exceptions
    - `NotADirectoryError`: If `dir1` or `dir2` is not a directory

    ## Docs
    - may not work for directories containing non-text items such as images/videos
    """
    
    ## Checks
    if not os.path.isdir(dir1): raise NotADirectoryError(f'Value `dir1` is not a directory: {repr(dir1)}.')
    if not os.path.isdir(dir2): raise NotADirectoryError(f'Value `dir2` is not a directory: {repr(dir2)}.')

    try:
        _compare(dir1, dir1, dir2)  # dir1 side
        _compare(dir2, dir2, dir1)  # dir2 side
    except AssertionError:
        return False
    
    return True