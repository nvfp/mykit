import tkinter as _tk
import typing as _typing

from mykit.app._runtime import Runtime as _Rt
from mykit.app.button import Button as _Button
from mykit.app.label import Label as _Label
from mykit.app.slider import _Slider


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


        ## <runtime>
        self._left_mouse_press = []
        self._left_mouse_hold = []
        self._left_mouse_release = []

        self._setup = None
        self._teardown = None
        ## </runtime>

    def listen(self, to: str, do: _typing.Callable[[], None]):
        """add event listener"""
        pass

    def setup(self, funcs: list[_typing.Callable[[], None]]):
        self._setup = funcs

    def teardown(self, funcs: list[_typing.Callable[[], None]]):
        self._teardown = funcs

    def run(self):
        
        ## <listeners>

        def left_mouse_press(e):
            _Button.press_listener()
        self.root.bind('<ButtonPress-1>', left_mouse_press)

        def left_mouse_hold(e):
            pass
        self.root.bind('<B1-Motion>', left_mouse_hold)

        def left_mouse_release(e):
            _Button.release_listener()
        self.root.bind('<ButtonRelease-1>', left_mouse_release)

        def repeat50():
            _Button.hover_listener()
            self.root.after(50, repeat50)

        self.root.bind('<Escape>', lambda e: self.root.destroy())

        ## </listeners>

        ## setup
        for fn in self._setup:
            fn()

        ## run
        self.root.mainloop()

        ## teardown
        for fn in self._teardown:
            fn()