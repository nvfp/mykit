import re as _re
import subprocess as _sp
from typing import (
    NoReturn as _NoReturn,
    Optional as _Optional,
    Union as _Union,
)


def run(commands: str, /, cwd:_Optional[str]=None) -> _Union[None, _NoReturn]:
    """
    A helper to use the `subprocess.run` function

    ## Examples
    - `run('echo 123')` is equal to `subprocess.run(['echo', '123'], cwd=None, check=True)`
    """
    cmds = _re.sub(r'[ ]+', ' ', commands.strip()).split(' ')
    _sp.run(cmds, cwd=cwd, check=True)