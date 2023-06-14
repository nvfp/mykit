import numpy as _np
from typing import (
    Tuple as _Tuple,
    Union as _Union
)


def tanh(x: _Union[float, _np.ndarray], /, derivative: bool = False) -> _Union[float, _np.ndarray]:

    z = _np.tanh(x)

    if derivative:
        return 1 - z*z
    else:
        return z

def sigmoid(x: _Union[float, _np.ndarray], /, derivative: bool = False) -> _Union[float, _np.ndarray]:

    z = 1 / (1 + _np.exp(-x))

    if derivative:
        return z*(1 - z)
    else:
        return z

def relu(x: _Union[float, _np.ndarray], /, derivative: bool = False) -> _Union[float, _np.ndarray]:

    if derivative:
        return _np.where(x > 0, 1, 0)
    else:
        return _np.maximum(0, x)


def get_angle(origin_x: float, origin_y: float, x: float, y: float, in_radians: bool = True) -> float:
    """
    Calculate the angle between two points (origin_x, origin_y) and (x, y) relative to the vertical axis.
    The x-axis is positive to the right, and the y-axis is positive upwards.

    ---

    ## Params
    - `in_radians`: Determines whether the angle is returned in radians (default) or degrees.
        
    ## Returns
    - Angle relative to vertical axis (CCW)

    ## Demo
    >>> print(get_angle(0, 0, 0, 1, False))
    0.0
    >>> print(get_angle(0, 0, -1, 0, False))
    90.0
    >>> print(get_angle(0, 0, 0, -1, False))
    180.0
    >>> print(get_angle(0, 0, 1, 0 , False))
    270.0
    >>> print(get_angle(0, 0, -1, 1 , False))
    45.0
    """

    dx = x - origin_x
    dy = y - origin_y

    ## Quadrant I (top left)
    if (dx <= 0) and (dy > 0):
        angle = _np.arctan2(-dx, dy)
    
    ## Quadrant II (down left)
    elif (dx < 0) and (dy <= 0):
        angle = _np.pi/2 + _np.arctan2(-dy, -dx)

    ## Quadrant III (down right)
    elif (dx >= 0) and (dy < 0):
        angle = _np.pi + _np.arctan2(dx, -dy)
    
    ## Quadrant IV (down right)
    elif (dx > 0) and (dy >= 0):
        angle = _np.pi*3/2 + _np.arctan2(dy, dx)

    if not in_radians:
        angle = _np.degrees(angle)

    return angle


def rotate(x: float, y: float, ctrx: float, ctry: float, a: float) -> _Tuple[float, float]:
    """
    Rotate points `(x, y)` around a center point `(ctrx, ctry)` by a given angle `a` in radians (CCW).
    The x-axis is positive to the right, and the y-axis is positive upwards.
    """

    ## translate the coordinate to the origin
    translated_x = x - ctrx
    translated_y = y - ctry

    ## apply the rotation transformation
    rotated_x = translated_x*_np.cos(a) - translated_y*_np.sin(a)
    rotated_y = translated_x*_np.sin(a) + translated_y*_np.cos(a)

    ## translate the coordinate back to its original position
    final_x = rotated_x + ctrx
    final_y = rotated_y + ctry

    return final_x, final_y