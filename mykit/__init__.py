import argparse as _argparse


__version__ = '9.1.0'


def _main():

    ## Main parsers
    p = _argparse.ArgumentParser()

    ## Global optional args
    p.add_argument('-v', '--version', action='version', version=f'mykit-{__version__}')

    args = p.parse_args()  # Run the parser
