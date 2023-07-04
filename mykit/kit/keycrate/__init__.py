import re as _re
import os as _os
from typing import (
    Any as _Any,
    Dict as _Dict,
    List as _List,
    NoReturn as _NoReturn,
    Tuple as _Tuple,
    Union as _Union
)

from mykit.kit.path import open_file as _open_file
from mykit.kit.utils import is_valid_var_name as _is_valid_var_name


class KeyCrate:
    """
    Using a .txt file (which is easy to open, read, and modify)
    to store key-value pairs, aiming to keep it simple and fast.
    """

    def __init__(
        self,
        file_pth: str,
        /,
        key_is_var: bool = False,
        eval_value: bool = False,
        only_keys: _Union[_List[str], _Tuple[str, ...], None] = None,
        need_keys: _Union[_List[str], _Tuple[str, ...], None] = None
    ) -> None:
        """
        Storing key-value pairs (key: value) in the .txt file `file_pth`.
        Access the value using either the class-like way (`kc.key`)
        or the dictionary-like way (`kc['key']`).

        ---

        ## Params
        - `file_pth`: full path to the .txt file that holds the key-value pairs
        - `key_is_var`: if `True`, all keys must be valid as variable name
        - `eval_value`: if `True`, all values must be evaluatable by `eval()`
        - `only_keys`: only keys specified by `only_keys` are allowed in `file_pth`
        - `need_keys`: keys that specified by `need_keys` must exist in `file_pth`

        ## Exceptions
        - `ValueError`: if `file_pth` is not a .txt file
        - `FileNotFoundError`: if `file_pth` is not a file
        - `AttributeError`: if trying to access a nonexistent key
        - see `self.parse` exceptions

        ## Demo 1
        >>> kc = KeyCrate('config.txt', eval_value=True)
        >>> fps = kc.fps  # or kc['fps']
        >>> output_dir = kc['output folder']

        ## Demo 2
        >>> settings = KeyCrate('settings.txt', key_is_var=True, only_keys=['fps', 'dur'])
        >>> fps = settings.fps
        >>> dur = settings.dur
        """

        ## keycrate file should be a .txt file
        if not file_pth.endswith('.txt'):
            raise ValueError(f'KeyCrate file {repr(file_pth)} should be a .txt file.')

        ## keycrate file must exist
        if not _os.path.isfile(file_pth):
            raise FileNotFoundError(f'KeyCrate file {repr(file_pth)} is not found.')


        ## added the prefix "_kc__" to prevent conflicts with the keys

        self._kc__file_pth = file_pth
        self._kc__key_is_var = key_is_var
        self._kc__eval_value = eval_value

        self._kc__only_keys = only_keys
        if type(only_keys) is tuple:
            self._kc__only_keys = list(only_keys)

        self._kc__need_keys = need_keys
        if type(need_keys) is tuple:
            self._kc__need_keys = list(need_keys)


        ## init
        self.parse()

    def __getattr__(self, __name: str, __default: _Any = None, /) -> _NoReturn:
        """This method is called when attribute `__name` is not found"""
        raise AttributeError(f'KeyCrate file {repr(self._kc__file_pth)} does not have key {repr(__name)}.')

    def __getitem__(self, __key: str, /) -> _Any:
        """
        To access the keys in a dictionary-like way (e.g., `kc['key1']`),
        it is commonly used for keys that are not variable names (e.g., `kc['full name']`).
        """
        return getattr(self, __key)

    def _read(self) -> str:
        """Return the current content of the file."""
        with open(self._kc__file_pth, 'r') as fp:
            out = fp.read()
        return out

    def parse(self) -> None:
        """
        If necessary, rerun this function to reparse.

        ---

        ## Exceptions
        - `SyntaxError`: if invalid syntax is found
        - `ValueError`: if any duplicate keys are found
        - `AssertionError`: if key is invalid for variable name (when `key_is_var=True`)
        - `AssertionError`: if value can't be evaluated (when `eval_value=True`)
        - `AssertionError`: if unexpected key is found (only when `only_keys` is specified)
        - `AssertionError`: if missing key is found (only when `need_keys` is specified)
        """

        raw = self._read()

        if self._kc__need_keys is not None:
            _need_keys = self._kc__need_keys.copy()

        for line_no, line in enumerate(raw.split('\n'), 1):

            if (line == '') or _re.match(r'\s*#--.*', line):
                ## blank-line or comment-header
                continue

            res = _re.match(
                r'\s*(?P<key>.+?)\s*:\s*(?P<val>.+?)\s*(?:#--.*)?;',
                ## added ";" to capture "everything" in `val` (but not
                ## the *last-spaces and comment* after it). The pattern doesn't
                ## work without it
                line + ';'
            )
            if res is None:
                raise SyntaxError(
                    f'KeyCrate file {repr(self._kc__file_pth)} '
                    f'has invalid syntax at line {line_no}: {repr(line)}'
                )

            key = res.group('key')
            val = res.group('val')

            if key in self.__dict__:
                raise ValueError(
                    f'KeyCrate file {repr(self._kc__file_pth)} '
                    f'has a duplicated key {repr(key)} found at line {line_no}.'
                )

            if self._kc__key_is_var:
                if not _is_valid_var_name(key):
                    raise AssertionError(
                        f'KeyCrate file {repr(self._kc__file_pth)} '
                        f'has a key {repr(key)} that is invalid for a variable name, found at line {line_no}.'
                    )

            if self._kc__eval_value:
                try:
                    val = eval(val, {})
                except (NameError, SyntaxError):
                    raise AssertionError(
                        f'KeyCrate file {repr(self._kc__file_pth)} '
                        f'has a value {repr(val)} that cannot be evaluated, found at line {line_no}.'
                    )

            if self._kc__only_keys is not None:
                if key not in self._kc__only_keys:
                    raise AssertionError(
                        f'KeyCrate file {repr(self._kc__file_pth)} '
                        f'has an unexpected key {repr(key)} found at line {line_no}.'
                    )

            if self._kc__need_keys:
                try:
                    _need_keys.remove(key)
                except ValueError:
                    ## note that if `need_keys` is specified, other keys
                    ## (not in `need_keys`) are also allowed.
                    ## so, this exception must be handled
                    pass

            setattr(self, key, val)

        if self._kc__need_keys:
            if _need_keys != []:
                raise AssertionError(
                    f'KeyCrate file {repr(self._kc__file_pth)} is missing keys: '
                    + ', '.join(map(repr, _need_keys))
                )

    def open(self) -> None:
        """open the .txt file"""
        _open_file(self._kc__file_pth)
    
    def export(self) -> _Dict[str, _Any]:
        """Return all the key-value pairs as dictionary."""

        force_copy = eval(str(self.__dict__), {})  # not sure gonna copy all the things deeply

        out = {
            key: force_copy[key]
            for key in filter(lambda key: not key.startswith('_kc__'), force_copy.keys())
        }
        return out