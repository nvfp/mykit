#!/usr/bin/env python
import argparse

from mykit import __version__, LIB_NAME


def main():

    parser = argparse.ArgumentParser(prog=LIB_NAME)
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s-{__version__}')

    args = parser.parse_args()  # run the parser


if __name__ == '__main__':
    main()