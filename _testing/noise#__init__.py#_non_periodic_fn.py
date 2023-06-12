import math
import tkinter as tk

from carbon.gui.slider import Slider
from carbon.noise import _non_periodic_fn
from carbon.graph.graph2d import graph2d


root = tk.Tk()
root.attributes('-fullscreen', True)

mon_width = root.winfo_screenwidth()
mon_height = root.winfo_screenheight()

page = tk.Canvas(width=mon_width, height=mon_height, bg='#111', highlightthickness=0, borderwidth=0)
page.place(x=0, y=0)

Slider.set_page(page)
Slider.set_page_focus([None])


class Rt:  # runtime
    nsample = 5000
    a = 1
    b = 1
    c = 1
    d = 1
    e = 1
    f = 1
    g = 1

def redraw():
    page.delete('graph2d')

    p = []
    for x in range(Rt.nsample):
        p.append((x, _non_periodic_fn(x*math.pi/180, Rt.a, Rt.b, Rt.c, Rt.d, Rt.e, Rt.f, Rt.g)))
    
    WIDTH = mon_width*0.7
    HEIGHT = mon_height*0.8
    graph2d(
        page,
        p,
        pos=((mon_width - WIDTH)*0.85, (mon_height - HEIGHT)/2),
        width=WIDTH,
        height=HEIGHT
    )

    page.create_text(
        mon_width/2, 30,
        text=f'{Rt.a}({Rt.b}sin({Rt.c}x) + {Rt.d}sin({Rt.e}*π*x) + {Rt.f}sin({Rt.g}*e*x))',
        font='Consolas 16', fill='#ddd', tags='graph2d'
    )

redraw()  # init

X = 130
Y = 50
GAP = 60
def fn(var):
    setattr(Rt, var, Slider.get_value_by_id(var))
    redraw()
Slider(
    id='nsample',
    min=50,
    max=10000,
    step=50,
    init=Rt.nsample,
    x=X,
    y=Y,
    fn=lambda: fn('nsample'),
    label='nsample',
    label_y_shift=-20
)
for idx, var in enumerate(['a', 'b', 'c', 'd', 'e', 'f', 'g'], 1):
    Slider(
        id=var,
        min=-3,
        max=3,
        step=0.01,
        init=getattr(Rt, var),
        x=X,
        y=Y + GAP*idx,
        fn=lambda var=var: fn(var),
        label=var,
        label_y_shift=-20
    )


def left_mouse_press(e):
    Slider.press_listener()    
root.bind('<ButtonPress-1>', left_mouse_press)

def left_mouse_hold(e):
    Slider.hold_listener()
root.bind('<B1-Motion>', left_mouse_hold)

def left_mouse_release(e):
    Slider.release_listener()
root.bind('<ButtonRelease-1>', left_mouse_release)

def background():
    Slider.hover_listener()
    root.after(50, background)
background()

root.bind('<Escape>', lambda e: root.destroy())
root.mainloop()