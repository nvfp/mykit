#!/usr/bin/env python
import argparse
import os
import sys

try:
    from mykit import __version__, LIB_NAME
except ModuleNotFoundError:
    ## This is done to handle situations where the 'mykit' isn't installed yet, so it can't be accessed.
    root_pth = os.path.dirname(os.path.dirname(__file__))
    sys.path.append(root_pth)
    from mykit import __version__, LIB_NAME


def main():

    parser = argparse.ArgumentParser(prog=LIB_NAME)
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s-{__version__}')

    args = parser.parse_args()  # run the parser


if __name__ == '__main__':
    main()