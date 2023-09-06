import os as _os
import re as _re
import shutil as _shutil
import subprocess as _sp
import sys as _sys
import tempfile as _tempfile
from typing import (
    Dict as _Dict,
)

from mykit.kit.fileops.simple import list_dir as _list_dir


## Supported dependencies
SUPPORTED_DEPS = {
    'mykit': 'https://github.com/nvfp/mykit.git',
    'pyggc': 'https://github.com/scapeville/py-git-ghcli.git',
}


class MyProg:  # My Program
    """
    ## The reason for the birth of this module is:
    - To avoid using "venv" library, which adds extra steps to the program installation process.
    - Very easy and versatile downloading (users can install the program globally without
        worrying about conflicts with global installations of the dependencies, as their versions might change over time).
    - Don't need to compile the entire program into an executable (just the entry point), which reduces file sizes.

    ## The aim of this module:
    - Users just have to run `pip install <program_name>`, and instantly, everything is downloaded perfectly with no dependency errors forever.

    ## Docs
    - The supported dependencies should adhere to these guidelines:
        - The Git tag (for release/production) should be in the format X.X.X (e.g., 1.0.0, 2.2.0).
        - The endpoint module should consist of two things: '__init__.py' and optionally 'test.py'.
        - It should have a 'lock_version' function at the root of the library.
    """

    def __init__(self, dist_dir:str, dependencies:_Dict[str, str]) -> None:
        """
        ## Params
        - `dist_dir`: The absolute path to the distribution folder (production folder) where it's published on PyPI.
        - `dependencies`: The format is: `{name: version}`, where "version" represents the Git tag of the dependency.
        """
        
        ## Checks
        if not _os.path.isdir(dist_dir): raise NotADirectoryError(f'Not a dir: {repr(dist_dir)}.')
        if len(dependencies) == 0: raise ValueError(f'MyProg essentially used with at least 1 dependency.')
        for k, v in dependencies.items():
            if k not in SUPPORTED_DEPS: raise ValueError(f'Not supported: {repr(k)}.')
            if not _re.match(r'\d+\.\d+\.\d+', v): raise ValueError(f'Invalid version: {repr(v)}.')

        self.dist_dir = dist_dir
        self.dependencies = dependencies

    def bundle_the_dependencies(self):
        """
        This function will bundle dependencies.
        Run this during the build process before publishing to production.

        ## Example
        - Run `python path/to/lib/dist_dir/__init__.py bundle`

        ## Docs
        - Run with the parameter "bundle" to prevent the script from accidentally running outside of the build process.
        """
        
        ## Checks
        def checks():
            ## Check the command
            if not ( (len(_sys.argv) == 2) and (_sys.argv[1] == 'bundle') ):
                raise AssertionError('It should be `python path/to/lib/dist_dir/__init__.py bundle` for bundling the dependencies.')
            ## Check the dir good to install
            # for dep in self.dependencies.keys():
            #     pth = _os.path.join(self.dist_dir, dep)
            #     if _os.path.isdir(pth):
            #         raise AssertionError(f"Can't bundle dependency {repr(dep)} because the folder already exists.")
            if _os.path.isdir(_os.path.join(self.dist_dir, '__myprog__')):
                raise AssertionError('__myprog__ folder already exists.')
        checks()  # wrapped by a function to prevent name conflicts

        # ## Temp
        # dir = _tempfile.mkdtemp()

        # for dep, ver in self.dependencies.items():
        #     _sp.run(['git', 'clone', '--depth', '1', '--branch', ver, SUPPORTED_DEPS[dep]], cwd=dir, check=True)

        #     ## TODO: make this more flexible
        #     if dep == 'mykit':
        #         _shutil.move(_os.path.join(dir, 'mykit', 'mykit'), _os.path.join(self.dist_dir, 'mykit'))
        #     if dep == 'pyggc':
        #         _shutil.move(_os.path.join(dir, 'py-git-ghcli', 'pyggc'), _os.path.join(self.dist_dir, 'pyggc'))

        ## Scan
        # def scan():
        #     def run(pth):
        #         for name, path in _list_dir(pth):
        #     run(self.dist_dir)
        # scan()
