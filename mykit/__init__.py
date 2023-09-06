from typing import (
    NoReturn as _NoReturn,
    Union as _Union,
)


__version__ = None  # This value will be written during the build process before production.


def lock_version(version:str, /) -> _Union[None, _NoReturn]:
    """Will raise `AssertionError` if the versions don't match"""
    if version != __version__:
        raise AssertionError(f"The `mykit` version {__version__} doesn't match the expected {version}.")
