from mykit.kit.color import (
    Hex as _Hex,
    Colored as _Colored
)
from mykit.kit.utils import printer as _printer


def _print_log(level, color, msg):
    _printer(_Colored(level, color) + ': ' + msg)


class pL:
    """pL (Print Log): A simple logger using Python's `print` function."""

    def debug(__msg: str, /) -> None:
        _print_log('DEBUG', _Hex.WHEAT, __msg)

    def info(__msg: str, /) -> None:
        _print_log('INFO', _Hex.BLUE_GRAY, __msg)

    def warning(__msg: str, /) -> None:
        _print_log('WARNING', _Hex.DARK_ORANGE, __msg)

    def error(__msg: str, /) -> None:
        _print_log('ERROR', _Hex.SCARLET, __msg)