import argparse

from . import __version__


def main():

    ## Main parsers
    p = argparse.ArgumentParser()

    ## Global optional args
    p.add_argument('-v', '--version', action='version', version=f'mykit-{__version__}')

    args = p.parse_args()  # Run the parser


if __name__ == '__main__':
    main()
