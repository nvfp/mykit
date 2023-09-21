import time as _time
import tkinter as _tk
from typing import (
    Any as _Any,
    Callable as _Callable,
    Dict as _Dict,
    List as _List,
)

from mykit.app.button import Button as _Button
from mykit.app.label import Label as _Label
from mykit.app.slider import _Slider

from mykit.app.complex.plot import Plot as _Plot
from mykit.app.complex.biplot import Biplot as _Biplot
from mykit.app.arrow import Arrow as _Arrow

from mykit.app.photoimg import PhotoImg


def _install_components(app):
    PhotoImg._install(app)


class App:
    """
    A single-page app framework.

    ## Limitations
    - Currently available only in fullscreen mode
    """

    def __init__(
        self,
        name: str = 'app',
        bg: str = '#111111',
    ) -> None:

        self.root = _tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.title(name)

        ## App's main page
        self.page = _tk.Canvas(
            master=self.root,
            width=self.root.winfo_screenwidth(),
            height=self.root.winfo_screenheight(),
            background=bg,
            borderwidth=0, highlightthickness=0
        )
        self.page.place(x=0, y=0)


        ## <register the page>
        
        ## widgets
        _Button._set_page(self.page)
        _Slider._set_page(self.page)

        ## others
        _Arrow._set_page(self.page)
        _Plot._set_page(self.page)
        _Biplot._set_page(self.page)

        ## </register the page>


        _install_components(self)


        ## <constants>

        self.T = _time.time()  # The timestamp when the app instance was initiated, usually used as the startup time.
        self.MON_WIDTH = self.root.winfo_screenwidth()
        self.MON_HEIGHT = self.root.winfo_screenheight()
        
        ## </constants>


        ## <runtime>

        self._left_mouse_press = []
        self._left_mouse_hold = []
        self._left_mouse_release = []

        self._background_processes = {}

        self._after_initialization = []
        self._dependencies = {}

        self._setup = []
        self._teardown = []

        ## </runtime>

    def listen(self, to:str, do:_Callable[[_tk.Event], None]) -> None:
        """
        Add event listener.

        ## Params
        - `to`: event type:
            - `"left-mouse-press"` or `"lmp"`
            - `"left-mouse-hold"` or `"lmh"`
            - `"left-mouse-release"` or `"lmr"`

        ## Docs
        - `do` function takes 1 positional parameter, which is a tkinter event object
        """
        
        if to in {'left-mouse-press', 'lmp'}:
            self._left_mouse_press.append(do)
        elif to in {'left-mouse-hold', 'lmh'}:
            self._left_mouse_hold.append(do)
        elif to in {'left-mouse-release', 'lmr'}:
            self._left_mouse_release.append(do)
        else:
            ValueError(f'Invalid event: {repr(to)}.')

    def add_background_processes(self, every: int, do: _Callable[[], None]) -> None:
        """
        Execute `do` every `every` milliseconds.
        
        ## Docs
        - The first execution occurs immediately after the app runs.
        """
        if every not in self._background_processes:
            self._background_processes[every] = []
        self._background_processes[every].append(do)

    def setup(self, funcs: _List[_Callable[[], None]]) -> None:
        """Running simple-functions right before startup."""
        self._setup = funcs

    def teardown(self, funcs: _List[_Callable[[], None]]) -> None:
        """Running simple-functions right after the app stops."""
        self._teardown = funcs

    def use(self, component: _Callable[..., None], /, dependencies: _Dict[str, _Any]) -> None:
        """This function helps make the dataflow easier to read."""
        component(**dependencies)

    def after_initialization_use(self, component: _Callable[..., None], /, *, with_dependencies: _List[str]) -> None:
        """Use `component` once all dependencies are ready."""
        self._after_initialization.append([component, with_dependencies])

    def add_dependencies(self, dependency: _Any, /) -> None:
        """Adds a dependency and should be used with the `after_initialization_use` method."""
        name = dependency.__name__
        if name in self._dependencies:
            raise ValueError(f'Dependency {repr(name)} is already added.')
        self._dependencies[name] = dependency

    def run(self):

        ## <internal>

        self.listen(to='left-mouse-press', do=_Button._press_listener)
        self.listen(to='left-mouse-press', do=_Slider._press_listener)

        self.listen(to='left-mouse-hold', do=_Slider._hold_listener)

        self.listen(to='left-mouse-release', do=_Button._release_listener)
        self.listen(to='left-mouse-release', do=_Slider._release_listener)

        self.add_background_processes(every=50, do=_Button._hover_listener)
        self.add_background_processes(every=50, do=_Slider._hover_listener)

        ## </internal>


        ## <listeners>

        self.root.bind('<ButtonPress-1>',   lambda e: [f(e) for f in self._left_mouse_press])
        self.root.bind('<B1-Motion>',       lambda e: [f(e) for f in self._left_mouse_hold])
        self.root.bind('<ButtonRelease-1>', lambda e: [f(e) for f in self._left_mouse_release])

        self.root.bind('<Escape>', lambda e: self.root.destroy())

        ## </listeners>


        def run_background_processes():
            def wrapper(dur, funcs):
                def inner():
                    for fn in funcs: fn()
                    self.root.after(dur, inner)
                return inner
            for dur, funcs in self._background_processes.items():
                fn = wrapper(dur, funcs)
                fn()  # start immediately
        run_background_processes()


        ## Initialize components that need to be initialized after all dependencies are ready
        for component, dependencies in self._after_initialization:
            component(self, **{d: self._dependencies[d] for d in dependencies})


        ## Setup
        for function in self._setup:
            function()

        ## Startup
        self.root.mainloop()

        ## Teardown
        for function in self._teardown:
            function()
