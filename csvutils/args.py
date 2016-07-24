#
# Provide a consistent argparser api
#

import argparse
import sys

def default_arguments():
    """
    Returns ArgumentParser with args used in all utils
    :return ArgumentParser:     ArgumentParser object
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', nargs='?',
        type=argparse.FileType('r'),
        default=sys.stdin)
    parser.add_argument('-d', '--delim',
        nargs='?',
        default=',')
    parser.add_argument('-N', '--no-header',
        action='store_false',
        dest='header')
    return parser
