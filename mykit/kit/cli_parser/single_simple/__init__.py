import sys as _sys
from typing import (
    Callable as _Callable
)

from mykit.kit.color import (
    Colored as _Colored,
    Hex as _Hex,
)
from mykit.kit.readable.box import box as _box


def _show_help_msg(software, version, repository, cmds):  # dev-docs: the code is a bit messy but compact, it's perfect.
    H = 'show this message then exit'
    longest = max([len(i) for i in cmds.keys()])  # Length of longest command name
    cmds_help = ''
    for name, (_, desc) in cmds.items():
        ## The extra space at the end is one-space padding
        cmds_help += f"   {_Colored(software + ' ' + name, _Hex.CORN)}{' '*(longest-len(name))} -> {_Colored(desc, _Hex.CORN)} \n"
    cmds_help += f"   {_Colored(software, _Hex.CORN)} {' '*longest} -> {_Colored(H, _Hex.CORN)} \n"
    msg = _box(
        '\n'
        ' Commands: \n'  # The extra space at the end is one-space padding (just in case `cmds_help` length < this line length)
        f'{cmds_help}'
        '\n'
        f' Info:\n'
        f'   software  : {software} \n'  # The extra space at the end is one-space padding
        f'   version   : {version} \n'
        f'   repository: {repository} \n'
    )
    print('\n' + msg)


class SingleSimple:
    """
    A simple tool for parsing arguments from the command line, designed to accept just 1 positional argument.

    ## Examples
    >>> myprogram # This will print the help message
    >>> myprogram command_1 # This will run the function associated with command_1
    >>> myprogram command_2 # This will run the function associated with command_2
    """

    def __init__(self, name:str, version:str, repo:str) -> None:
        """
        ## Params
        - `name`: software/program name
        - `version`: software version
        - `repo`: software source code

        ## Docs
        - There is no validation process, such as checking if the command
            name should not be empty, should not be duplicated, etc. So
            please handle that manually.
        - Also, there are no extreme case validations, such as when no
            command was given, etc. Please handle it manually.
        """
        self.name = name
        self.version = version
        self.repo = repo
        self.cmds = {}

    def add(self, cmd:str, run:_Callable[[], None], desc:str) -> None:
        """
        ## Params
        - `cmd`: command name (which will be used like `myprogram <cmd>`)
        - `run`: function to be fired when `cmd` executed
        - `desc`: description of the command
        """
        self.cmds[cmd] = [run, desc]


    def _run_inner(self, args, is_testing):  # Created for testing purposes

        ## Handle show-help
        if len(args) == 1:
            _show_help_msg(self.name, self.version, self.repo, self.cmds)
            if is_testing: return
            _sys.exit(0)

        cmd = args[1]

        ## Handle invalid command
        if cmd not in self.cmds:
            print(f'Unknown commands {repr(cmd)}, run `{self.name}` for help.')
            if is_testing: return
            _sys.exit(1)

        ## Run the corresponding function
        self.cmds[cmd][0]()

    def run(self) -> None:
        """Listen to the command line and run the requested command."""
        args = _sys.argv
        self._run_inner(args, False)
