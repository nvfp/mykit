"""
This module is for internal use purposes only.
"""
import tkinter as tk


class Runtime:

    ## reminder: the `page` is accessible, while `_set_page` is intended for internal use only
    page: tk.Canvas = None
    @staticmethod
    def _set_page(page: tk.Canvas, /) -> None:
        Runtime.page = page