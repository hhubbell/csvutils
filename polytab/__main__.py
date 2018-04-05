#
# Provide a consistent argparser api
#

from __future__ import absolute_import
from . import polytab, parsers
import argparse
import csv
import pkg_resources
import statistics
import sys


MAP_FUNCTIONS = {
    'mean': statistics.mean,
    'sum': sum
}

def map(args, remainder):
    """
    Command line utility to map a function to a tabular file
    """
    informat = getattr(parsers, args.informat)(designation='inparser')
    outformat = getattr(parsers, args.outformat)(designation='outparser')

    informat.parse_args(remainder)
    outformat.parse_args(remainder)

    fn = MAP_FUNCTIONS[args.function]
    cols, avgs = zip(*polytab.fmap(informat.file, fn,
        parser=informat,
        columns=args.cols))

    if args.precision:
        avgs = ['{:.{}f}'.format(x, args.precision) for x in avgs]

    if args.transpose is True:
        if args.alphabetize is True:
            outformat.rows = sorted(zip(cols, avgs), key=lambda x: x[0])
        else:
            outformat.rows = zip(cols, avgs)
    else:
        outformat.header = cols
        outformat.rows = [avgs]

    outformat.write(outformat.file)

def convert(args, remainder):
    """
    Command line utility to convert one tabular format to another
    """
    informat = getattr(parsers, args.informat)(designation='inparser')
    outformat = getattr(parsers, args.outformat)(designation='outparser')

    informat.parse_args(remainder)
    outformat.parse_args(remainder)

    polytab.convert(informat.file, informat, outformat).write(outformat.file)

def drop(args, remainder):
    """
    Command line utility to drop columns from a tabular file
    """
    informat = getattr(parsers, args.informat)(designation='inparser')
    informat.parse_args(remainder)

    header, rows = polytab.drop(informat.file,
        parser=informat,
        columns=args.cols)

    informat.header = header
    informat.rows = rows
    informat.designation = 'outparser'
    informat.parse_args(remainder)
    informat.write(informat.file)

def keep(args, remainder):
    """
    Command line utiltiy to keep columns in a tabular file. The inverse of `drop`
    """
    informat = getattr(parsers, args.informat)(designation='inparser')
    informat.parse_args(remainder)

    header, rows = polytab.keep(informat.file,
        parser=informat,
        columns=args.cols)

    informat.header = header
    informat.rows = rows
    informat.designation = 'outparser'
    informat.parse_args(remainder)
    informat.write(informat.file)

def tab(args, remainder):
    """
    Command line utility to tabulate a csv file for easy viewing
    """
    informat = getattr(parsers, args.informat)(designation='inparser')
    outformat = parsers.table()

    informat.parse_args(remainder)
    outformat.parse_args(remainder)

    outformat.rows = polytab.tabulate(informat.file,
        parser=informat,
        maxw=outformat.column_maxwidth,
        pad=outformat.padding)

    outformat.write(outformat.file)

def main():
    """
    Set up argparse interface and call given subparser
    """
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-h', '--help',
        nargs='?',
        action=CSVUtilsHelpAction,
        help='Show this help message and exit.')
    parser.add_argument('-f', '--from',
        dest='informat',
        nargs='?',
        default='csv',
        help='Input file type. Default CSV.')
    parser.add_argument('-v', '--version',
        action='version',
        version=pkg_resources.get_distribution(__package__).version,
        help='Print version number and exit.')

    subparsers = parser.add_subparsers(dest='func')

    # polytab map
    fmap = subparsers.add_parser('map')
    fmap.add_argument('function',
        choices=MAP_FUNCTIONS.keys(),
        help='Function to apply across all records of a column')
    fmap.add_argument('-c', '--cols', nargs='*',
        help='A list of columns. Each column will have an average generated.')
    fmap.add_argument('-a', '--alphabetize',
        action='store_true',
        help='A flag to indicate the output should be displayed in ' \
            'alphabetical order. This argument is only valid if the output ' \
            'is transposed. Equivalent to `csvavg ... -T | sort`.')
    fmap.add_argument('-p', '--precision',
        type=int,
        help='The number of decimal places to show.')
    fmap.add_argument('-t', '--to',
        dest='outformat',
        nargs='?',
        default='csv',
        help='Output file type. Default CSV.')
    fmap.add_argument('-T', '--transpose',
        action='store_true',
        help='A flag to indicate the output should be transposed so that ' \
            'there are two columns and N rows, where N equals the number ' \
            'of columns indicated to average.')

    # polytab convert
    convert = subparsers.add_parser('convert')
    convert.add_argument('-t', '--to',
        dest='outformat',
        nargs='?',
        default='csv',
        help='Output file type. Default CSV.')

    #polytab drop
    drop = subparsers.add_parser('drop')
    drop.add_argument('-c', '--cols', nargs='*',
        help='A list of columns. Each column listed will be dropped.')

    # polytab keep
    keep = subparsers.add_parser('keep')
    keep.add_argument('-c', '--cols', nargs='*',
        help='A list of columns. Each column listed will be kept.')

    # polytab tab
    tab = subparsers.add_parser('tab')
 
    # `parse_known_args` is causing problems with `set_defaults`, so use
    # `dest` instead. This just means a little extra work on our end.
    args, remainder = parser.parse_known_args()
    getattr(sys.modules[__name__], args.func)(args, remainder)


class CSVUtilsHelpAction(argparse.Action):

    def __call__(self, parser, namespace, value, option_string):
        if value is None:
            parser.print_help()
        else:
            fileparser = getattr(parsers, value)()
            fileparser._inparser.print_help()
            fileparser._outparser.print_help()

        parser.exit()


if __name__ == '__main__':
    main()
