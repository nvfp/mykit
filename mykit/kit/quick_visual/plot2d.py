import tkinter as _tk

from mykit.kit.graph.graph2d import Graph2D as _Graph2D


def plot2d(
    points: list[tuple[float, float]],
    xspan = 0.80,
    yspan = 0.65,
    cfg: dict = {}
):
    """`cfg`: extra configurations for Graph2D"""

    root = _tk.Tk()
    root.attributes('-fullscreen', True)

    mon_width = root.winfo_screenwidth()
    mon_height = root.winfo_screenheight()

    page = _tk.Canvas(width=mon_width, height=mon_height, bg='#121212', highlightthickness=0, borderwidth=0)
    page.place(x=0, y=0)

    _Graph2D.set_page(page)


    WIDTH = mon_width*xspan
    HEIGHT = mon_height*yspan
    TL_X = (mon_width - WIDTH)/2
    TL_Y = (mon_height - HEIGHT)/2
    _Graph2D(points, width=WIDTH, height=HEIGHT, tl_x=TL_X, tl_y=TL_Y, **cfg)


    root.bind('<Escape>', lambda e: root.destroy())
    root.mainloop()