import sys as _sys
import os as _os
import re as _re


class Ctxt:  # Born: 2023 Dec 29
    """
    ## Usage
    - colored = Ctxt('foo', '#ff0000')

    this one same as the one in `kit`, btw, but more standalone.
    """

    _RESET = '\033[0m'  # note, "\033" is the same as "\x1b"

    win_init = False

    @staticmethod
    def _hex_to_rgb(c):
        return tuple(int(c.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    
    @staticmethod
    def _lcut(input_str, unwanted):
        if input_str.startswith(unwanted):
            return input_str[len(unwanted):]
        else:
            return input_str
    
    @staticmethod
    def _rcut(input_str, unwanted):
        if input_str.endswith(unwanted):
            return input_str[:-len(unwanted)]
        else:
            return input_str

    def __new__(text:str, foreground:str, background=None) -> str:
        """
        ## Params
        - `foreground`, `background`: must in "#RRGGBB" format.

        ## Usage
        - colored = Ctxt('foo', '#ff0000')
        """
        if _sys.platform.lower() == 'win32':
            if not Ctxt.win_init:
                _os.system('color')
                Ctxt.win_init = True
        text = str(text)
        fg_r, fg_g, fg_b = Ctxt._hex_to_rgb(foreground)
        header = '\033[' + f'38;2;{fg_r};{fg_g};{fg_b}'
        if background is not None:
            bg_r, bg_g, bg_b = Ctxt._hex_to_rgb(background)
            header += f';48;2;{bg_r};{bg_g};{bg_b}'    
        header += 'm'
        if text.endswith(Ctxt._RESET):
            text = Ctxt._rcut(text, Ctxt._RESET)
        text = _re.sub(r'\033\[0m(?!\033\[38;2)', Ctxt._RESET+header, text)
        text = _re.sub(r'(?<!\033\[0m)\033\[38;2', Ctxt._RESET+'\033[38;2', text)
        if text.startswith(Ctxt._RESET):
            text = Ctxt._lcut(text, Ctxt._RESET)
            the_header = ''
        else:
            the_header = header
        return the_header + text + Ctxt._RESET
