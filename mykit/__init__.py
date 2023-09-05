import argparse as _argparse
from typing import (
    NoReturn as _NoReturn,
    Union as _Union,
)


__version__ = '9.1.0'


def lock_version(version:str, /) -> _Union[None, _NoReturn]:
    """Will raise `AssertionError` if the versions don't match"""
    if version != __version__:
        raise AssertionError(f"The `mykit` version {__version__} doesn't match the expected {version}.")


def _main():

    ## Main parsers
    p = _argparse.ArgumentParser()

    ## Global optional args
    p.add_argument('-v', '--version', action='version', version=f'mykit-{__version__}')

    args = p.parse_args()  # Run the parser
