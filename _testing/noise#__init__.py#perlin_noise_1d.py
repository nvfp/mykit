import math
import tkinter as tk
import random

from carbon.gui.slider import Slider
from carbon.noise import perlin_noise_1d
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
    nsample = 100
    persistence = 0.5
    octaves = 1
    frequency = 2
    seed = 0

def redraw():
    page.delete('graph2d')

    p = []
    for x in range(Rt.nsample):
        p.append((x, perlin_noise_1d(x, Rt.persistence, Rt.octaves, Rt.frequency, Rt.seed)))

    WIDTH = mon_width*0.7
    HEIGHT = mon_height*0.8
    graph2d(
        page,
        p,
        pos=((mon_width - WIDTH)*0.85, (mon_height - HEIGHT)/2),
        width=WIDTH,
        height=HEIGHT,
        title='1D Perlin noise',
        title_font='Verdana 21'
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
    min=5,
    max=5000,
    step=1,
    init=Rt.nsample,
    x=X,
    y=Y + GAP*0,
    fn=lambda: fn('nsample'),
    label='nsample',
    label_y_shift=-20
)
Slider(
    id='persistence',
    min=0,
    max=1,
    step=0.01,
    init=Rt.persistence,
    x=X,
    y=Y + GAP*1,
    fn=lambda: fn('persistence'),
    label='persistence',
    label_y_shift=-20
)
Slider(
    id='octaves',
    min=1,
    max=10,
    step=1,
    init=Rt.octaves,
    x=X,
    y=Y + GAP*2,
    fn=lambda: fn('octaves'),
    label='octaves',
    label_y_shift=-20
)
Slider(
    id='frequency',
    min=1,
    max=10,
    step=1,
    init=Rt.frequency,
    x=X,
    y=Y + GAP*3,
    fn=lambda: fn('frequency'),
    label='frequency',
    label_y_shift=-20
)
Slider(
    id='seed',
    min=-25,
    max=25,
    step=1,
    init=Rt.seed,
    x=X,
    y=Y + GAP*4,
    fn=lambda: fn('seed'),
    label='seed',
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