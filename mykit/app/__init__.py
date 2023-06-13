import tkinter as _tk

from mykit.app._runtime import Runtime as _Rt


class App(_Rt):
    """
    Single-page app.

    ---

    ## Limitations
    - currently available only in fullscreen mode
    """

    def __init__(self, title: str, bg: str) -> None:
        
        self.root = _tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.title(title)

        page = _tk.Canvas(
            master=self.root,
            width=self.root.winfo_screenwidth(),
            height=self.root.winfo_screenheight(),
            background=bg,
            borderwidth=0, highlightthickness=0
        )
        page.place(x=0, y=0)
        App.page = page


        ## runtime

    def add_listener():
        pass

    ## this function can't exist because once listeners are added, they might be complicated to remove
    # def remove_listener():
    #     pass

    def run(self):
        
        ## listeners

        def left_mouse_press(e):
            Button.press_listener()
            if draw_pad.paint() and Runtime.realtime:
                show_result()
        root.bind('<ButtonPress-1>', left_mouse_press)

        def left_mouse_hold(e):
            if draw_pad.paint() and Runtime.realtime:
                show_result()
        root.bind('<B1-Motion>', left_mouse_hold)

        def left_mouse_release(e):
            Button.release_listener()
        root.bind('<ButtonRelease-1>', left_mouse_release)

        def background_fast():
            Button.hover_listener()
            root.after(50, background_fast)

        def exit(e):
            root.destroy()
            printer('INFO: Exited.')
        root.bind('<Escape>', exit)

        self.root.mainloop()