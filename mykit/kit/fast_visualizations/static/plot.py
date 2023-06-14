from typing import (
    List as _List,
    Tuple as _Tuple,
)

from mykit.app import App as _App
from mykit.app.complex.plot import Plot as _Plot


def plot(
    points: _List[_Tuple[float, float]],
    xspan = 0.80,
    yspan = 0.65,
    cfg: dict = {}
):
    """`cfg`: extra configurations"""

    app = _App()

    WIDTH = app.MON_WIDTH*xspan
    HEIGHT = app.MON_HEIGHT*yspan
    TL_X = (app.MON_WIDTH - WIDTH)/2
    TL_Y = (app.MON_HEIGHT - HEIGHT)/2
    _Plot(points, width=WIDTH, height=HEIGHT, tl_x=TL_X, tl_y=TL_Y, **cfg)

    app.run()