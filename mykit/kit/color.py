

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
        '#7f007f'
        >>> interpolate_color('#ff0000', '#0000ff', 1.0)
        '#0000ff'
    """
    ## convert color strings to RGB values
    r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
    r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)

    ## interpolate RGB values based on x
    r = int(r1 + (r2 - r1)*x)
    g = int(g1 + (g2 - g1)*x)
    b = int(b1 + (b2 - b1)*x)

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