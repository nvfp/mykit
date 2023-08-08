import subprocess as _sp

from mykit.kit.color import (
    Colored as _Colored,
    Hex as _Hex,
)
from mykit.kit.time import TimeFmt as _TimeFmt


def _logger(level, color, msg):
    _sp.run(['echo', f'[{_TimeFmt.hour()}] {_Colored(level, color)}: {msg}'])


class eL:
    """
    eL (`echo` Log): A simple logger using `echo` function,
    intended for use within GitHub Action virtual machines.
    Inspired by `mykit.kit.pLog.pL`.
    """

    @staticmethod
    def group(name:str, /) -> None:
        _sp.run(['echo', f'::group::{name}'])

    @staticmethod
    def endgroup(name:str='', /) -> None:
        """
        ## Params
        - `name`: doesn't do anything, just for readability.
        
        ## Demo
        >>> eL.group('group-a')
        >>> eL.endgroup()
        >>> eL.group('group-b')
        >>> eL.endgroup('group-b')
        """
        _sp.run(['echo', '::endgroup::'])

    @staticmethod
    def debug(msg:str, /) -> None:
        _logger('DEBUG', _Hex.WHEAT, msg)

    @staticmethod
    def info(msg:str, /) -> None:
        _logger('INFO', _Hex.BLUE_GRAY, msg)

    @staticmethod
    def warning(msg:str, /) -> None:
        _logger('WARNING', _Hex.DARK_ORANGE, msg)

    @staticmethod
    def error(msg:str, /) -> None:
        _logger('ERROR', _Hex.SCARLET, msg)