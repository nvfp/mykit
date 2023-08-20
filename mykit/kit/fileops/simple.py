"""
Most of the functions here are standalone
"""
import os as _os
import re as _re


def same_ext_for_all_dir_files(dir_path:str, extension:str) -> bool:
    """
    Check whether all files in `dir_path` have the same `extension`.
    Return `True` if they are all the same, and `False` if not.

    ### Conditions
    - All items in folder `dir_path` are files only; no subfolders.

    ### Params
    - `dir_path`: absolute path to the directory
    - `extension`: file type (including the dot), example: `'.txt'`, `'.py'`.

    ### Exceptions
    - `NotADirectoryError`: if `dir_path` is not a folder
    - `ValueError`: if `extension` doesn't match the regex
    - `FileNotFoundError`: if an item in the folder is not a file

    ### Docs
    - Will return `True` when `dir_path` is empty
    - Will ignore case: `.json` matches `.JSON`, `.TxT` matches `.Txt`, and so on.
    """
    if not _os.path.isdir(dir_path): raise NotADirectoryError(f'Not a dir: {repr(dir_path)}.')
    if not _re.match(r'^\.\w+$', extension): raise ValueError(f'Invalid extension: {repr(extension)}.')
    for file in _os.listdir(dir_path):
        pth = _os.path.join(dir_path, file)
        if not _os.path.isfile(pth): raise FileNotFoundError(f'Not a file: {repr(pth)}.')
        if not file.lower().endswith(extension.lower()): return False
    return True