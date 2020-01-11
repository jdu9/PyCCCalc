from pycccalc.__init__ import (
    __version__,
    __author__,
    __email__,
    __description__
)

import argparse
import sys


def parser(argv):
    parser = argparse.ArgumentParser(
        prog="pycccalc",
        description=__description__
    )

    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version='%(prog)s ' + __version__
    )

    parser.add_argument(
        '-a',
        '--author',
        action='version',
        version='%(prog)s made by ' + __author__ + ' (' + __email__ + ')',
        help="show program's author and exit"
    )

    parser.add_argument(
        "-d",
        "--decimals",
        type=int,
        help="Set number of decimals for the result.",
        default=11
    )

    parser.add_argument(
        "--variables",
        type=str,
        help='Pass variables as json.',
        default='{"pi": 3.141592653589793, "solution": 42}'
    )

    return parser.parse_args(argv)


def main():
    args = parser(sys.argv[1:])

    from pycccalc import app
    return app.run(args)
