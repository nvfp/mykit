import os as _os
import re as _re
import sys as _sys
from typing import (
    Optional as _Optional,
    Tuple as _Tuple
)


def interpolate_color(color1: str, color2: str, x: float) -> str:
    """
    Interpolates between two colors based on the given ratio `x`.

    ---

    ## Params
    - `color1`: The first color in hexadecimal format (e.g., '#RRGGBB').
    - `color2`: The second color in hexadecimal format (e.g., '#RRGGBB').
    - `x`: The ratio determining the interpolation between the two colors. Should be between 0 and 1.

    ## Returns
    - The interpolated color as a hexadecimal string.

    ## Demo
    >>> interpolate_color('#ff0000', '#0000ff', 0.0)
    '#ff0000'
    >>> interpolate_color('#ff0000', '#0000ff', 0.5)
    '#800080'
    >>> interpolate_color('#ff0000', '#0000ff', 1.0)
    '#0000ff'
    """
    ## convert color strings to RGB values
    r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
    r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)

    ## interpolate RGB values based on x
    r = round(r1 + (r2 - r1)*x)
    g = round(g1 + (g2 - g1)*x)
    b = round(b1 + (b2 - b1)*x)

    ## convert interpolated RGB values to hexadecimal color string
    interpolated_color = f'#{r:02x}{g:02x}{b:02x}'
    return interpolated_color


def getgray(alpha: float, /, max_lum: int = 255) -> str:
    """
    Returns a hexadecimal color value representing a grayscale shade based on the given alpha and maximum luminance.

    ---

    ## Params
    - `alpha`: A grayscale shade intensity value in the range [0, 1].
    - `max_lum`: Maximum luminance value for grayscale in the range [0, 255].

    ## Demo
    >>> getgray(0.5)
    '#808080'
    """
    a = f'{round(max_lum*alpha):02x}'
    return f'#{a}{a}{a}'


def hex_to_rgb(hex_color: str, /) -> _Tuple[int, int, int]:
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(r: int, g: int, b: int, /) -> str:
    return f'#{r:02x}{g:02x}{b:02x}'


def hexa_to_hex(foreground: str, opacity: float, background: str) -> str:
    """
    Calculates the hexadecimal color code of `foreground` with the given `opacity` on `background`.
    The `foreground` and `background` must be valid hexadecimal color codes,
    and the `opacity` value must be in the interval [0, 1].
    """

    fg = [int(foreground[i:i+2], 16) for i in (1, 3, 5)]
    bg = [int(background[i:i+2], 16) for i in (1, 3, 5)]

    r = round(fg[0]*opacity + bg[0]*(1 - opacity))
    g = round(fg[1]*opacity + bg[1]*(1 - opacity))
    b = round(fg[2]*opacity + bg[2]*(1 - opacity))

    return f'#{r:02x}{g:02x}{b:02x}'


def interpolate_with_black(foreground: str, opacity: float) -> str:
    """
    This is the optimized version of `hexa_to_hex(foreground, opacity, '#000000')`.
    Please refer to the documentation of the `hexa_to_hex` function for more details.
    """

    c = [int(foreground[i:i+2], 16) for i in (1, 3, 5)]

    r = round( c[0]*opacity )
    g = round( c[1]*opacity )
    b = round( c[2]*opacity )

    return f'#{r:02x}{g:02x}{b:02x}'


class Hex:
    """List of colors in hexadecimal format."""

    ## Basic

    BLACK = '#000000'
    WHITE = '#ffffff'
    RED = '#ff0000'
    LIME = '#00ff00'
    BLUE = '#0000ff'
    YELLOW = '#ffff00'
    CYAN = '#00ffff'
    MAGENTA = '#ff00ff'
    SILVER = '#c0c0c0'
    GRAY = '#808080'
    MAROON = '#800000'
    OLIVE = '#808000'
    GREEN = '#008000'
    PURPLE = '#800080'
    TEAL = '#008080'
    NAVY = '#000080'

    ## Source: https://en.wikipedia.org/wiki/List_of_colors:_A%E2%80%93F

    ALABASTER = '#edebe0'
    AMBER = '#ffc000'
    ARYLIDE_YELLOW = '#ead76c'
    ASH_GRAY = '#b3c0b6'
    ATOMIC_TANGERINE = '#ff9966'
    AUBURN = '#a62929'
    AUREOLIN = '#fdee00'
    AZURE = '#0080ff'

    BEIGE = '#f5f5dc'
    BITTERSWEET = '#ff715f'
    BLACK_OLIVE = '#3b3d36'
    BLEU_DE_FRANCE = '#318de9'
    BLIZZARD_BLUE = '#ace6ee'
    BLUE_GRAY = '#669acd'
    BLUSH = '#df5c83'
    BOTTLE_GREEN = '#006c4f'
    BRIGHT_MAROON = '#c22147'
    BURGUNDY = '#800021'
    BURNT_ORANGE = '#cc5400'
    BURNT_SIENNA = '#e87352'

    CADMIUM_ORANGE = '#ed872e'
    CAMEL = '#c2996b'
    CAPRI = '#00c0ff'
    CARDINAL = '#c41f3b'
    CARIBBEAN_GREEN = '#00cd9a'
    CAROLINA_BLUE = '#57a1d4'
    CHAMPAGNE = '#f7e8cf'
    CITRINE = '#e4d20a'
    CORAL = '#ff7e4f'
    CORN = '#faed5c'

    DARK_ORANGE = '#ff8c00'
    DARK_RED = '#8c0000'
    DIM_GRAY = '#696969'

    ELECTRIC_BLUE = '#7dfaff'
    EMERALD = '#4fc778'

    FALU_RED = '#801717'
    FLAME = '#e45a21'
    FIREBRICK = '#b32121'

    GO_GREEN = '#00ab66'
    GRANITE_GRAY = '#666666'

    HARLEQUIN = '#40ff00'

    IVORY = '#fffff1'

    JADE = '#00a96c'

    LAPIS_LAZULI = '#26619c'
    LAVENDER_GRAY = '#c4c2d1'
    LAWN_GREEN = '#7dfc00'
    LIGHT_GRAY = '#d4d4d4'
    LIGHT_GREEN = '#8fed8f'
    LIGHT_YELLOW = '#ffffe0'
    LILAC = '#c7a3c7'
    LINEN = '#faf0e5'
    LISERAN_PURPLE = '#de70a1'

    MANATEE = '#9799ac'
    MAUVE = '#e1b1ff'
    MYSTIC = '#d75283'

    OPAL = '#a8c2bd'
    OUTRAGEOUS_ORANGE = '#ff6e4a'

    PEACH = '#ffe6b6'

    RASPBERRY = '#e40a5c'
    RUBY = '#e0125e'
    RUST = '#b8400d'

    SAND = '#c3b380'
    SAPPHIRE = '#0f52bb'
    SCARLET = '#ff2400'
    SEA_GREEN_CRAYOLA = '#00ffcc'
    SEASHELL = '#fff5ed'
    SUNGLOW = '#ffcd33'

    TAN = '#d2b68d'

    WHEAT = '#f6dfb3'

    ## Custom

    TERMINAL = '#0c0c0c'
    GRAY30 = '#1e1e1e'

    LAVENDER_BLISS = '#d0adf0'  # Very soft violet


class Colored:
    """
    ## Test
    >>> from mykit.kit.color import Colored, Hex
    >>> for k, v in Hex.__dict__.items():
    >>>     if k.startswith('__'): continue
    >>>     print(Colored(k, v))
    """

    _win_init = False  # To make it work in Windows command prompt
    _RESET = '\033[0m'

    def __new__(
        cls,
        text:str,
        /,
        fg:str=Hex.MANATEE,
        bg:_Optional[str]=None
    ) -> str:
        """
        Return the colored version of `text`.

        ---

        ## Params
        - `fg`: foreground color in hexadecimal format
        - `bg`: background color in hexadecimal format; if not specified,
                the default terminal background color will be used.
        """

        ## Windows users
        if _sys.platform.lower() == 'win32':
            if not Colored._win_init:
                _os.system('color')
                Colored._win_init = True

        text = str(text)
        fg_r, fg_g, fg_b = hex_to_rgb(fg)

        ## Refs: - https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
        ##       - https://gist.github.com/Abraxos/f491670c85fd76bfeb7067cb8ea1acf7
        header = (
            '\033['
            f'38;2;{fg_r};{fg_g};{fg_b}'
        )

        if bg is not None:
            bg_r, bg_g, bg_b = hex_to_rgb(bg)
            header += f';48;2;{bg_r};{bg_g};{bg_b}'

        header += 'm'

        ## Handle multiple colors in one string
        if cls._RESET in text:
            text = text.replace(cls._RESET, header)

        return header + text + cls._RESET


def colored_len(text:str, /) -> int:
    """
    Count the text length produced by `Colored` (also works for nested `Colored`).

    ## Demo
    >>> colored_len(Colored('hi'))  # 2
    >>> colored_len('12'+ Colored('34') + '56')  # 6
    >>> colored_len(Colored('12' + Colored('34', Hex.RED)))  # 4
    """
    original_len = len(text)
    c1 = _re.findall(r'\033\[38;2;\d{1,3};\d{1,3};\d{1,3}(?:;48;2;\d{1,3};\d{1,3};\d{1,3})?m', text)
    c2 = _re.findall(r'\033\[0m', text)
    color_len = sum([len(i) for i in c1+c2])
    return original_len - color_len
