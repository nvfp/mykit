import sys as _sys
from typing import (
    Callable as _Callable
)


def _show_help_msg():
    pass


class SingleSimple:

    def __init__(self, name:str, version:str, repo:str) -> None:
        self.name = name
        self.version = version
        self.repo = repo
        self.cmds = {}

    def add(self, cmd:str, run:_Callable[[], None], desc:str) -> None:
        self.cmds[cmd] = [run, desc]

    def run(self) -> None:
        
        args = _sys.argv

        ## Handle show-help
        if len(args) == 1:
            _show_help_msg()
            _sys.exit(0)

        cmd = args[1]

        ## Handle invalid command
        if cmd not in self.cmds:
            print(f'Unknown commands {repr(cmd)}, run `{self.name}` for help.')
            _sys.exit(1)

        ## Run the corresponding function
        self.cmds[cmd][0]()
