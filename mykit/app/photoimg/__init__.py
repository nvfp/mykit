import tkinter as _tk
from typing import (
    Callable as _Callable,
    Dict as _Dict,
    List as _List,
    Literal as _Literal,
    Optional as _Optional,
    Tuple as _Tuple,
    Union as _Union
)


class _Rt:  # Runtime

    installed = False
    
    p: _tk.Canvas = None  # App's main page

    instances = {}  # Identified using ID
    groups    = {}  # Identified using tag


class PhotoImg:

    @staticmethod
    def _install(app):
        """Fully standalone installation function to plug this component into the app."""
        _Rt.installed = True
        _Rt.p = app.page

    def __init__(self,
        id: _Optional[str] = None,
        tags: _Optional[_Union[str, _List[str], _Tuple[str, ...]]] = None,
    ) -> None:

        ## Validations
        if not _Rt.installed: raise AssertionError("This component hasn't been installed yet.")

    def annihilate(self) -> None:
        """Completely remove it as if it never existed before."""  # dev-docs: use "it" so i dont have to change it for each class
        pass
