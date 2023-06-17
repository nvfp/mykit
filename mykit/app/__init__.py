import tkinter as _tk
from typing import (
    Callable as _Callable,
    List as _List
)

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

    def __init__(
        self,
        name: str = 'app',
        bg: str = '#111111'
    ) -> None:

        self.root = _tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.title(name)

        page = _tk.Canvas(
            master=self.root,
            width=self.root.winfo_screenwidth(),
            height=self.root.winfo_screenheight(),
            background=bg,
            borderwidth=0, highlightthickness=0
        )
        page.place(x=0, y=0)
        App._set_page(page)


        ## <constants>
        self.MON_WIDTH = self.root.winfo_screenwidth()
        self.MON_HEIGHT = self.root.winfo_screenheight()
        ## </constants>


        ## <runtime>
        self._left_mouse_press = []
        self._left_mouse_hold = []
        self._left_mouse_release = []

        self._background_processes = {}

        self._setup = []
        self._teardown = []
        ## </runtime>

    def listen(self, to: str, do: _Callable[[_tk.Event], None]):
        """
        Add event listener.

        ---

        ## Params
        - `to`: `Literal["left-mouse-press", "left-mouse-hold", "left-mouse-release"]`

        ## Docs
        - `do` function takes 1 positional parameter, which is a tkinter event object
        """
        
        if to == 'left-mouse-press':
            self._left_mouse_press.append(do)
        elif to == 'left-mouse-hold':
            self._left_mouse_hold.append(do)
        elif to == 'left-mouse-release':
            self._left_mouse_release.append(do)
        else:
            ValueError(f'Invalid event: {repr(to)}.')
    
    def add_background_processes(self, every: int, do: _Callable[[], None]) -> None:
        """
        Execute `do` every `every` milliseconds.
        The first execution occurs immediately after the app runs.
        """
        if every in self._background_processes:
            self._background_processes[every].append(do)
        else:
            self._background_processes[every] = [do]

    def setup(self, funcs: _List[_Callable[[], None]]):
        self._setup = funcs

    def teardown(self, funcs: _List[_Callable[[], None]]):
        self._teardown = funcs

    def run(self):
        
        ## <listeners>

        def left_mouse_press(e):
            
            ## internal
            _Button.press_listener()
            _Slider.press_listener()
            
            ## external
            for fn in self._left_mouse_press:
                fn(e)

        self.root.bind('<ButtonPress-1>', left_mouse_press)

        def left_mouse_hold(e):
            
            ## internal
            _Slider.hold_listener()

            ## external
            for fn in self._left_mouse_hold:
                fn(e)

        self.root.bind('<B1-Motion>', left_mouse_hold)

        def left_mouse_release(e):

            ## internal
            _Button.release_listener()
            _Slider.release_listener()

            ## external
            for fn in self._left_mouse_release:
                fn(e)
        self.root.bind('<ButtonRelease-1>', left_mouse_release)

        self.root.bind('<Escape>', lambda e: self.root.destroy())

        ## </listeners>


        ## <background processes>

        ## internal
        def repeat50():
            _Button.hover_listener()
            _Slider.hover_listener()
            self.root.after(50, repeat50)
        # self.root.after(50, repeat50)  # start after 50ms
        repeat50()  # start immediately

        ## users
        def setup_background_processes():
            def wrapper(dur, funcs):
                def inner():
                    for fn in funcs: fn()
                    self.root.after(dur, inner)
                return inner
            for dur, funcs in self._background_processes.items():
                fn = wrapper(dur, funcs)
                fn()  # start immediately
        setup_background_processes()
        
        ## </background processes>


        ## setup
        for fn in self._setup: fn()

        ## run
        self.root.mainloop()

        ## teardown
        for fn in self._teardown: fn()