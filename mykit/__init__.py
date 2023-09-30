from typing import (
    NoReturn as _NoReturn,
    Union as _Union,
)

from mykit.inventory.builder import builder as _builder
from mykit.kit.cli_parser.single_simple import SingleSimple as _SingleSimple


__version__ = None  # This value will be written during the build process before production.


def lock_version(version:str, /) -> _Union[None, _NoReturn]:
    """Will raise `AssertionError` if the versions don't match"""
    if version != __version__:
        raise AssertionError(f"The `mykit` version {repr(__version__)} doesn't match the expected {repr(version)}.")


def _main():
    
    p = _SingleSimple('mykit', __version__, 'https://github.com/nvfp/mykit')
    p.add('build', 0)
