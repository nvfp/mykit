import sys as _sys
from typing import (
    NoReturn as _NoReturn,
)

from mykit.kit.keycrate import KeyCrate as _KeyCrate
from mykit.kit.path import open_file as _open_file


class Monoconfig:
    """
    A simple plugin to handle a centralized, single set of settings for a program.

    Ideally, you will have this folder inside your program source:
    ```txt
    settings/
    └─ __init__.py
    └─ settings.txt

    # settings/__init__.py
    import os
    from mykit.kit.scpp.monoconfig import Monoconfig
    SETTINGS_FILE_PTH = os.path.join(os.path.dirname(__file__), 'settings.txt')
    cfg = Monoconfig(SETTINGS_FILE_PTH)
    ```
    """

    def __init__(self, file_path:str) -> None:
        """
        ## Params
        - `file_path`: Absolute path to the settings/configurations file

        ## Docs
        - There's minimal validation, such as not checking whether `file_path` exists
            or not (please handle that manually). TODO: Add validations for critical ones.
        """
        self.file_path = file_path

    def load_these_settings(self, *keys):
        """
        ## Usage
        >>> cfg = Monoconfig('settings.txt')
        >>> CFG = cfg.load_these_settings('foo', 'bar')
        >>> CFG.foo  # Accessing key `foo`
        >>> CFG.bar  # Accessing key `bar`
        >>> cfg.open()  # Open settings file then exit program
        """
        try:
            cfg = _KeyCrate(self.file_path, True, True, need_keys=keys)
        except (ValueError, FileNotFoundError, AttributeError, SyntaxError, AssertionError) as err:
            print(f"There are invalid configurations in the settings. Please open the software settings to fix this error: {err}")
            _sys.exit(1)
        return cfg

    def open(self) -> _NoReturn:
        """Open the settings file then exit."""
        _open_file(self.file_path)
        _sys.exit(0)
