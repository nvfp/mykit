import tkinter as tk

from carbon.gui.button.v3 import Button
from carbon.gui.label.v2 import Label
from carbon.gui.slider.v2 import Slider, VSlider


root = tk.Tk()
root.attributes('-fullscreen', True)

mon_width = root.winfo_screenwidth()
mon_height = root.winfo_screenheight()

page = tk.Canvas(width=mon_width, height=mon_height, bg='#000', highlightthickness=0, borderwidth=0)
page.place(x=0, y=0)

Button.set_page(page)
Slider.set_page(page)


x = 200
y = 200
r = 3
page.create_oval(x-r, y-r, x+r, y+r, fill='#f00')

lbl = Label(x, y, '1. MAIN')
lbl = Label(text='2. next to MAIN').align(lbl)
lbl = Label(text='3. below').align(lbl, 'n', 's', 0, 0)
lbl = Label(text='4. below with gap').align(lbl, 'n', 's', 0, 15)
lbl = Label(text='5. TR corner to DL corner', bd_width=2).align(lbl, 'ne', 'sw', 0, 0)

btn = Button(label='6. Next to (5)').align(lbl)
btn = Button(label='7. below (6), click to print "123"', fn=lambda: print(123), width=250).align(btn, 'n', 's', 0, 10)
btn = Button(label='8. DR to TL').align(btn, 'nw', 'se', 10, 10)

sld = Slider().align(btn)
sld = Slider(1, 10, 2, 5, label='min=1, max=10, step=2, init=5', x=400, y=500)
sld = VSlider(1, 10, 2, 5).align(sld, 'n', 'e', 0, 0)
sld = Slider(
    rod_len=400,
    label='Foo',
    show_label_box=True,
    label_box_color='#333',
    label_box_width=100,
    label_box_height=20,
    label_y_shift=-30,
    # locked=True
).align(sld, 'w', 'e', 30, 0)


def left_mouse_press(e):
    Button.press_listener()    
    Slider.press_listener()    
root.bind('<ButtonPress-1>', left_mouse_press)

def left_mouse_hold(e):
    Slider.hold_listener()
root.bind('<B1-Motion>', left_mouse_hold)

def left_mouse_release(e):
    Button.release_listener()
    Slider.release_listener()
root.bind('<ButtonRelease-1>', left_mouse_release)


def background():
    Button.hover_listener()
    Slider.hover_listener()
    root.after(50, background)  # 20 FPS (recommended if using slider)
background()


root.bind('<Escape>', lambda e: root.destroy())
root.mainloop()