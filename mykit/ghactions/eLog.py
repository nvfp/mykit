import subprocess as _sp

from mykit.kit.color import (
    Hex as _Hex,
    Colored as _Colored
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

    def group(name:str, /) -> None:
        _sp.run(['echo', f'::group::{name}'])

    def endgroup() -> None:
        _sp.run(['echo', '::endgroup::'])

    def debug(msg:str, /) -> None:
        _logger('DEBUG', _Hex.WHEAT, msg)

    def info(msg:str, /) -> None:
        _logger('INFO', _Hex.BLUE_GRAY, msg)

    def warning(msg:str, /) -> None:
        _logger('WARNING', _Hex.DARK_ORANGE, msg)

    def error(msg:str, /) -> None:
        _logger('ERROR', _Hex.SCARLET, msg)