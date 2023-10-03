"""
Most of the functions here are standalone
"""
import os as _os
import re as _re
from typing import (
    List as _List,
    Tuple as _Tuple,
    Optional as _Optional,
    Union as _Union,
)


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
    - `AssertionError`: if an item in the folder is not a file

    ### Docs
    - Will return `True` when `dir_path` is empty
    - Will ignore case: `.json` matches `.JSON`, `.TxT` matches `.Txt`, and so on.
    """
    if not _os.path.isdir(dir_path): raise NotADirectoryError(f'Not a dir: {repr(dir_path)}.')
    if not _re.match(r'^\.\w+$', extension): raise ValueError(f'Invalid extension: {repr(extension)}.')
    for file in _os.listdir(dir_path):
        pth = _os.path.join(dir_path, file)
        if not _os.path.isfile(pth): raise AssertionError(f'Not a file: {repr(pth)}.')
        if not file.lower().endswith(extension.lower()): return False
    return True


def list_dir(dir_path:str, /) -> _List[_Tuple[str, str]]:
    """
    The extended version of `os.listdir`.

    @param `dir_path`: absolute path
    @returns: List of pairs of item names and the items' absolute paths,
              e.g., `[(file_name, file_abspath), (subdir_name, subdir_abspath), ...]`

    ### Exceptions
    - `NotADirectoryError`: if `dir_path` not a folder

    ### Demo
    ```
    for file_name, file_path in list_dir('/dir/abs/path'):
        pass
    for item, abspth in list_dir('/dir/abs/path'):
        pass
    for name, pth in list_dir('/dir/abs/path'):  # my favorite  ~Nicholas
        pass
    ```
    """
    if not _os.path.isdir(dir_path): raise NotADirectoryError(f'Not a dir: {repr(dir_path)}.')
    out = []
    for name in _os.listdir(dir_path):
        pth = _os.path.join(dir_path, name)
        out.append((name, pth))
    return out


def remove_all_specific_files_in(dir_path:str, file_pattern:str, recursive:bool=False) -> _List[str]:
    """
    Delete certain files within the `dir_path` folder.

    ---

    ## Params
    - `dir_path`: Absolute path to the folder
    - `file_pattern`: Regex pattern to match the files that you want to delete.
    - `recursive`: If `False`, just delete the files inside `dir_path`.

    ## Returns
    - List of deleted files' absolute paths.

    ## Docs
    - Please review the code for this function before using it.
    """
    deleted = []
    def run(pth):
        for stuff in _os.listdir(pth):
            stuff_pth = _os.path.join(pth, stuff)
            if _os.path.isdir(stuff_pth):
                if recursive: run(stuff_pth)
            else:
                if _re.match(file_pattern, stuff):
                    _os.remove(stuff_pth)
                    deleted.append(stuff_pth)
    run(dir_path)
    return deleted


def norm_pth(__pth:str, /, lowercasing:bool=False) -> str:
    r"""
    Normalizing path.

    ## Params
    - `__pth`: The path
    - `lowercasing`: normalize the case (into lowercase)

    ## Examples
    >>> norm_pth(r'/path/dir////file')  # \path\dir\file
    >>> norm_pth(r'/Path/dir/\/\/\file.TXT/', True)  # \path\dir\file.txt
    """
    if lowercasing: __pth = _os.path.normcase(__pth)
    return _os.path.normpath(__pth)


def definitely_a_dir(__pth:str, /) -> None:
    r"""
    Making sure the given path `__pth` is a directory and it exists

    ## Exceptions
    - `NotADirectoryError`: if not a dir

    ## Demo
    >>> normalized_pth = norm_pth(r'/foo//Bar/\\/\//myDir')
    >>> definitely_a_dir(normalized_pth)
    """
    if not _os.path.isdir(__pth): raise NotADirectoryError(f'Not a dir: {repr(__pth)}.')


def dont_worry_the_path_ends_with(__pth:str, /, suffixes:_Union[str, _List[str], _Tuple[str, ...]], ignore_case:bool=True) -> None:
    """
    Making sure the given path `__pth` ends with the given `suffixes`,
    or if `__pth` is a file path, it guarantees the file has the correct expected extension(s).

    ## Params
    - `__pth`: the path
    - `suffixes`: single or multiple suffixes
    - `ignore_case`: if `False`, ".jpg" is not the same as ".JPG"

    ## Exceptions
    - `ValueError`: if `suffixes` is an empty string
    - `AssertionError`: if the ending does not match the expected `suffixes`

    ## Examples
    - `dont_worry_the_path_ends_with('init_log.txt', '_log.txt')  # okay`
    - `dont_worry_the_path_ends_with('testfile.txt', '_log.txt')  # no`
    - `dont_worry_the_path_ends_with('file.txt', ('.txt', '.log'))  # okay`
    - `dont_worry_the_path_ends_with('file.log', ('.txt', '.log'))  # okay`
    - `dont_worry_the_path_ends_with('file.cpp', ('.txt', '.log'))  # no`
    - `dont_worry_the_path_ends_with('x.foo', ['.FOO', '.BAR'])  # okay`
    - `dont_worry_the_path_ends_with('x.FOO', ['.foo', '.bar'])  # okay`
    - `dont_worry_the_path_ends_with('x.Foo', '.foo', True)   # okay`
    - `dont_worry_the_path_ends_with('x.Foo', '.foo', False)  # no`

    ## Demo
    >>> normalized_pth = norm_pth(r'/foo//Bar/\\/\//file.TXt')
    >>> dont_worry_the_path_ends_with(normalized_pth, '.txt')
    """
    if suffixes == '': raise ValueError("`suffixes` shouldn't be an empty string.")
    
    if ignore_case:
        p_ = __pth.lower()
        if type(suffixes) is str:
            s_ = suffixes.lower()
        else:
            s_ = tuple([s.lower() for s in suffixes])
    else:
        p_ = __pth
        if type(suffixes) is str:
            s_ = suffixes
        else:
            s_ = tuple([s for s in suffixes])
    
    if not p_.endswith(s_):
        raise AssertionError(f'Invalid suffixes: [expected: {repr(suffixes)}] [got: {repr(__pth)}]')


def definitely_a_file(__path:str, /) -> None:
    """
    Making sure the given path is a file that also exists

    ## Exceptions
    - `FileNotFoundError`: if not a file path

    ## Demo
    >>> normalized_pth = norm_pth(r'/foo//Bar/\\/\//file.Txt', True)
    >>> dont_worry_the_path_ends_with(normalized_pth, '.txt')
    >>> definitely_a_file(normalized_pth)
    """
    if not _os.path.isfile(__path): raise FileNotFoundError(f"Not a file: {repr(__path)}.")


def this_path_must_not_exist(__path:str, /) -> None:
    """
    Make sure the given path is not a file, directory, etc.
    This is created to ensure that when performing writing operations, nothing will be overwritten.

    ## Exceptions
    - `AssertionError`: if already exists

    ## Demo
    >>> path_normalized = norm_pth(r'/foo//Bar/\\/\//file.Txt', True)
    >>> dont_worry_the_path_ends_with(path_normalized, '.txt')
    >>> this_path_must_not_exist(path_normalized)
    >>> # rest of the script
    """
    if _os.path.exists(__path): raise AssertionError(f"Already exists: {repr(__path)}.")
