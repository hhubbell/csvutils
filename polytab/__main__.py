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

    XXX: Broken with new CommonTable abstraction
    """
    reader = getattr(adapters, args.informat)('reader')
    writer = getattr(adapters, args.outformat)('writer')

    reader.parse_args(remainder)
    writer.parse_args(remainder)

    # Would be cool to do this in the `coupler` pipeline
    fn = MAP_FUNCTIONS[args.function]
    data = polytab.fmap(informat.file, fn,
        adapter=reader,
        columns=args.cols)

    # FIXME: Disable for now until type checker
    #if args.precision:
    #    avgs = ['{:.{}f}'.format(x, args.precision) for x in avgs]

    # FIXME: Disable for now
    #if args.transpose is True:
    #    if args.alphabetize is True:
    #        outformat.rows = sorted(zip(cols, avgs), key=lambda x: x[0])
    #    else:
    #        outformat.rows = zip(cols, avgs)
    #else:
    #    outformat.header = cols
    #    outformat.rows = [avgs]

    # FIXME
    writer.data = data
    writer.write(writer.file)

def convert(args, remainder):
    """
    Command line utility to convert one tabular format to another
    """
    reader = getattr(adapters, args.informat)('reader')
    writer = getattr(adapters, args.outformat)('writer')

    reader.parse_args(remainder)
    writer.parse_args(remainder)

    with polytab.coupler(reader, writer) as cpl:
        cpl.write(writer.file)

def drop(args, remainder):
    """
    Command line utility to drop columns from a tabular file
    """
    reader = getattr(adapters, args.informat)('reader')
    writer = getattr(adapters, args.informat)('writer')

    reader.parse_args(remainder)
    writer.parse_args(remainder)

    # Would be cool to do this in the `coupler` pipeline
    data = polytab.drop(informat.file,
        adapter=informat,
        columns=args.cols)

    with polytab.coupler(reader, writer) as cpl:
        # FIXME
        cpl.write(writer.file)

def keep(args, remainder):
    """
    Command line utiltiy to keep columns in a tabular file. The inverse of `drop`
    """
    reader = getattr(adapters, args.informat)('reader')
    writer = getattr(adapters, args.informat)('writer')

    reader.parse_args(remainder)
    writer.parse_args(remainder)

    # Would be cool to do this in the `coupler` pipeline
    data = polytab.keep(reader.file,
        adapter=informat,
        columns=args.cols)

    with polytab.coupler(reader, writer) as cpl:
        # FIXME
        cpl.write(writer.file)

def summarize(args, remainder):
    """
    Command line utility to summarize a tabular file.
    """
    reader = getattr(adapters, args.informat)('reader')
    writer = getattr(adapters, args.outformat)('writer')

    reader.parse_args(remainder)
    writer.parse_args(remainder)

    # would be cool to do this in the `coupler` pipeline
    data = polytab.summarize(reader.file, adapter=reader)
    
    with polytab.coupler(reader, writer) as cpl:
        # FIXME
        cpl.write(writer.file)

def tab(args, remainder):
    """
    Command line utility to tabulate a tabular file for easy viewing
    """
    reader = getattr(adapters, args.informat)('reader')
    writer = adapters.table('writer')

    reader.parse_args(remainder)
    writer.parse_args(remainder)

    with polytab.coupler(reader, writer) as cpl:
        # FIXME
        cpl.write(writer.file)

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
    # FIXME: Some options disabled until API consistency issues are resolved
    sp_map = subparsers.add_parser('map', parents=[p_adapter])
    sp_map.add_argument('function',
        choices=MAP_FUNCTIONS.keys(),
        help='Function to apply across all records of a column')
    sp_map.add_argument('-c', '--cols', nargs='*',
        help='A list of columns. Each column will have an average generated.')
    #sp_map.add_argument('-a', '--alphabetize',
    #    action='store_true',
    #    help='A flag to indicate the output should be displayed in ' \
    #        'alphabetical order. This argument is only valid if the output ' \
    #        'is transposed. Equivalent to piping to sort without any args.')
    #sp_map.add_argument('-p', '--precision',
    #    type=int,
    #    help='The number of decimal places to show.')
    sp_map.add_argument('-t', '--to',
        dest='outformat',
        nargs='?',
        default='csv',
        help='Output file type. Default CSV.')
    #sp_map.add_argument('-T', '--transpose',
    #    action='store_true',
    #    help='A flag to indicate the output should be transposed so that ' \
    #        'there are two columns and N rows, where N equals the number ' \
    #        'of columns indicated to average.')
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
    sp_summarize.add_argument('-t', '--to',
        dest='outformat',
        nargs='?',
        default='csv',
        help='Output file type. Default CSV.')
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
