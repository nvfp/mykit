import tkinter as tk

from carbon.gui.button.v3 import Button
from carbon.gui.label.v2 import Label


root = tk.Tk()
root.attributes('-fullscreen', True)

mon_width = root.winfo_screenwidth()
mon_height = root.winfo_screenheight()

page = tk.Canvas(width=mon_width, height=mon_height, bg='#000', highlightthickness=0, borderwidth=0)
page.place(x=0, y=0)

Button.set_page(page)


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


def left_mouse_press(e):
    Button.press_listener()    
root.bind('<ButtonPress-1>', left_mouse_press)

def left_mouse_release(e):
    Button.release_listener()
root.bind('<ButtonRelease-1>', left_mouse_release)


def background():
    Button.hover_listener()
    root.after(40, background)  # 25 FPS
background()


root.bind('<Escape>', lambda e: root.destroy())
root.mainloop()