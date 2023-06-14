import math as _math
import random as _random
import time as _time
from typing import (
    List as _List,
    Tuple as _Tuple
)


def _non_periodic_fn(__x: float, /, a: float = 1, b: float = 1, c: float = 1, d: float = 1, e: float = 1, f: float = 1, g: float = 1):
    """
    proven non-periodic.
    ref: https://stackoverflow.com/questions/8798771/perlin-noise-for-1d

    ---

    `__x` is in radian
    """
    return a*(b*_math.sin(c*__x) + d*_math.sin(e*_math.pi*__x) + f*_math.sin(g*_math.e*__x))

def random_sine_noise(
    seed: float,
    nsample: int,
    ymin: int,
    ymax: int,
    params: _Tuple = (1, 1, 1, 1, 1, 1, 1)
) -> _List[_Tuple[float, float]]:

    _random.seed(seed)
    shift = _random.randint(-1000000000, 1000000000)

    points = []
    for x in range(nsample):
        x += shift
        points.append((x, _non_periodic_fn(x*_math.pi/180, *params)))

    ## adjusting the y interval
    y_values = [point[1] for point in points]
    ymin_current = min(y_values)
    ymax_current = max(y_values)
    scale_factor = (ymax - ymin) / (ymax_current - ymin_current)
    points = [(x, ymin + (y - ymin_current)*scale_factor) for (x, y) in points]

    return points


def _pn1d_noise(x: int, seed: int) -> float:
    """Generate deterministic noise based on the given seed."""
    x = (x << 13) ^ x ^ seed
    return 1.0 - ((x * (x * x * 15731 + 789221) + 1376312589) & 0x7fffffff) / 1073741824.0

def _pn1d_noise_smoothed(x: int, seed: int) -> float:
    """combines multiple noise samples to compute the final value"""
    return _pn1d_noise(x, seed)/2 + _pn1d_noise(x - 1, seed)/4 + _pn1d_noise(x + 1, seed)/4

def _pn1d_noise_interpolated(x: int, seed: int) -> float:
    """using cubic interpolation"""
    int_x = int(x)
    frac_x = x - int_x

    v0 = _pn1d_noise_smoothed(int_x - 1, seed)
    v1 = _pn1d_noise_smoothed(int_x, seed)
    v2 = _pn1d_noise_smoothed(int_x + 1, seed)
    v3 = _pn1d_noise_smoothed(int_x + 2, seed)

    ## cubic interpolation
    p = (v3 - v2) - (v0 - v1)
    q = (v0 - v1) - p
    r = v2 - v0
    s = v1
    return p*frac_x*frac_x*frac_x + q*frac_x*frac_x + r*frac_x + s

def perlin_noise_1d(x: float, /, persistence: float = 0.5, octaves: int = 1, frequency: int = 2, seed: int = _time.time()) -> float:
    """
    Generate 1D Perlin noise for the given input parameters.
    ref: https://web.archive.org/web/20160530124230/http://freespace.virgin.net/hugo.elias/models/m_perlin.htm

    ---

    ## params
        `x`: input value.
        `persistence`: persistence value determining the amplitude decrease per octave.
        `octaves`: number of octaves or levels of detail in the Perlin noise.
        `frequency`: lower frequency results in higher detail.
        `seed`: seed value for randomness.

    ## returns
        float: Perlin noise value
    """
    total = 0
    for i in range(octaves):
        f = frequency**i
        amplitude = persistence**i
        total += amplitude*_pn1d_noise_interpolated(x*f, seed)
    return total
