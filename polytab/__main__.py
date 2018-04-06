#
# Provide a consistent argparser api
#

from __future__ import absolute_import
from . import polytab, adapters
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
    informat = getattr(adapters, args.informat)(designation='inparser')
    outformat = getattr(adapters, args.outformat)(designation='outparser')

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
    informat = getattr(adapters, args.informat)(designation='inparser')
    outformat = getattr(adapters, args.outformat)(designation='outparser')

    informat.parse_args(remainder)
    outformat.parse_args(remainder)

    polytab.convert(informat.file, informat, outformat).write(outformat.file)

def drop(args, remainder):
    """
    Command line utility to drop columns from a tabular file
    """
    informat = getattr(adapters, args.informat)(designation='inparser')
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
    informat = getattr(adapters, args.informat)(designation='inparser')
    informat.parse_args(remainder)

    header, rows = polytab.keep(informat.file,
        parser=informat,
        columns=args.cols)

    informat.header = header
    informat.rows = rows
    informat.designation = 'outparser'
    informat.parse_args(remainder)
    informat.write(informat.file)

def summarize(srgs, remainder):
    """
    Command line utility to summarize a tabular file.
    """
    informat = getattr(parsers, args.informat)(designation='inparser')
    outformat = getattr(parsers, args.outformat)(designation='outparser')

    informat.parse_args(remainder)
    outformat.parse_args(remainder)

    header, rows = polytab.summarize(informat.file, parser=informat)
    
    outformat.header = header
    outformat.rows = rows
    outformat.write(outformat.file)

def tab(args, remainder):
    """
    Command line utility to tabulate a csv file for easy viewing
    """
    informat = getattr(adapters, args.informat)(designation='inparser')
    outformat = adapters.table()

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
    parser.add_argument('-v', '--version',
        action='version',
        version=pkg_resources.get_distribution(__package__).version,
        help='Print version number and exit.')

    # Input adapter argument handler
    p_adapter = argparse.ArgumentParser(add_help=False)
    p_adapter.add_argument('-f', '--from',
        dest='informat',
        nargs='?',
        default='csv',
        help='Input file type. Default CSV.')

    subparsers = parser.add_subparsers()

    # polytab map
    sp_map = subparsers.add_parser('map', parents=[p_adapter])
    sp_map.add_argument('function',
        choices=MAP_FUNCTIONS.keys(),
        help='Function to apply across all records of a column')
    sp_map.add_argument('-c', '--cols', nargs='*',
        help='A list of columns. Each column will have an average generated.')
    sp_map.add_argument('-a', '--alphabetize',
        action='store_true',
        help='A flag to indicate the output should be displayed in ' \
            'alphabetical order. This argument is only valid if the output ' \
            'is transposed. Equivalent to piping to sort without any args.')
    sp_map.add_argument('-p', '--precision',
        type=int,
        help='The number of decimal places to show.')
    sp_map.add_argument('-t', '--to',
        dest='outformat',
        nargs='?',
        default='csv',
        help='Output file type. Default CSV.')
    sp_map.add_argument('-T', '--transpose',
        action='store_true',
        help='A flag to indicate the output should be transposed so that ' \
            'there are two columns and N rows, where N equals the number ' \
            'of columns indicated to average.')
    sp_map.set_defaults(func=map)

    # polytab convert
    sp_convert = subparsers.add_parser('convert', parents=[p_adapter])
    sp_convert.add_argument('-t', '--to',
        dest='outformat',
        nargs='?',
        default='csv',
        help='Output file type. Default CSV.')
    sp_convert.set_defaults(func=convert)

    #polytab drop
    sp_drop = subparsers.add_parser('drop', parents=[p_adapter])
    sp_drop.add_argument('-c', '--cols', nargs='*',
        help='A list of columns. Each column listed will be dropped.')
    sp_drop.set_defaults(func=drop)

    # polytab keep
    sp_keep = subparsers.add_parser('keep', parents=[p_adapter])
    sp_keep.add_argument('-c', '--cols', nargs='*',
        help='A list of columns. Each column listed will be kept.')
    sp_keep.set_defaults(func=keep)

    # polytab summarize
    sp_summarize = subparsers.add_parser('summarize', parents=[p_adapter])
    sp_summarize.set_defaults(func=summarize)

    # polytab tab
    sp_tab = subparsers.add_parser('tab', parents=[p_adapter])
    sp_tab.set_defaults(func=tab)
 
    # Call subparser function
    args, remainder = parser.parse_known_args()
    args.func(args, remainder)


class CSVUtilsHelpAction(argparse.Action):

    def __call__(self, parser, namespace, value, option_string):
        if value is None:
            parser.print_help()
        else:
            fileadapter = getattr(adapters, value)()
            fileadapter._inparser.print_help()
            fileadapter._outparser.print_help()

        parser.exit()


if __name__ == '__main__':
    main()
