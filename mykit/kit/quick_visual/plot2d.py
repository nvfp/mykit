import tkinter as _tk
from typing import Optional as _Optional

from carbon.graph.graph2d import graph2d as _graph2d


def plot2d(
    points: list[tuple[float, float]],
    xspan = 0.80,
    yspan = 0.65,
    graph2d_cfg: dict = {}
):

    root = _tk.Tk()
    root.attributes('-fullscreen', True)

    mon_width = root.winfo_screenwidth()
    mon_height = root.winfo_screenheight()

    page = _tk.Canvas(width=mon_width, height=mon_height, bg='#121212', highlightthickness=0, borderwidth=0)
    page.place(x=0, y=0)


    WIDTH = mon_width*xspan
    HEIGHT = mon_height*yspan
    TL_X = (mon_width - WIDTH)/2
    TL_Y = (mon_height - HEIGHT)/2
    _graph2d(page, points, width=WIDTH, height=HEIGHT, pos=(TL_X, TL_Y), **graph2d_cfg)


    root.bind('<Escape>', lambda e: root.destroy())
    root.mainloop()