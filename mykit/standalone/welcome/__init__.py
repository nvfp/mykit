import os
from datetime import datetime, timedelta, timezone
import platform, random


def welcome(gmt:float, root:str, Ctxt=None) -> None:  # Born: 2023 Dec 29
    """
    ## Params
    - `gmt`: GMT offset (in hours). Example: if UTC+0100 -> gmt=1; UTC-0230 -> gmt=-2.5
    - `root`: the abs path to the project's root directory (assuming there's `__main__.py` in the root folder).
    - `Ctxt`: is the `Ctxt` function from mykit (used for coloring). If none, will printed without color.
    """
    OS = platform.system()
    if OS == 'Windows': T = datetime.now().astimezone(timezone(timedelta(hours=gmt))).strftime('RUNNING @ %Y %b %#d, %H:%M:%S, UTC%z')
    elif OS == 'Darwin': T = datetime.now().astimezone(timezone(timedelta(hours=gmt))).strftime('RUNNING @ %Y %b %-d, %H:%M:%S, UTC%z')
    elif OS == 'Linux': T = datetime.now().astimezone(timezone(timedelta(hours=gmt))).strftime('RUNNING @ %Y %b %-d, %H:%M:%S, UTC%z')
    else: raise AssertionError(f"Unknown OS: {repr(OS)}.")
    PAD = 2  # number of spaces
    SEP = '─'*((os.get_terminal_size().columns-1-len(T)-PAD)//2)
    HEADER = f'{SEP} {T} {SEP}'
    GREET = random.choice(['Welcome!', 'Hello again...', 'Hi and welcome :)'])
    HELPER = f'python {os.path.relpath(root, os.getcwd())} ?'
    if Ctxt is None:
        print(
            HEADER + '\n' +
            GREET + '\n' +
            f"└── Run `{HELPER}` to see the Help message then exit."
        )
    else:
        print(
            Ctxt(HEADER, '#ff2400') + '\n' +
            GREET + '\n' +
            f"└── Run `{Ctxt(HELPER, '#f6dfb3')}` to see the Help message then exit."
        )
