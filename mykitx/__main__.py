import argparse

from carbon import LIB_VER, LIB_NAME_ONLY


def main():

    parser = argparse.ArgumentParser(prog=LIB_NAME_ONLY)
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s-{LIB_VER}')

    args = parser.parse_args()  # run the parser


if __name__ == '__main__':
    main()