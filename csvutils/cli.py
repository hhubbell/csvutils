#
# Provide a consistent argparser api
#

from __future__ import absolute_import
from . import csvutils, parsers
from .guts import helpers
import argparse
import csv
import pkg_resources
import sys


def _default_arguments(infiles='?'):
    """
    Returns ArgumentParser with args used in all utils
    :option infiles:            Specify the amount of infiles to expect.
                                Defaults to '?'
    :return ArgumentParser:     ArgumentParser object
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
    # XXX Allow global no-header? (sets both infile and outfile)
    # parser.add_argument('-N', '--no-header',
    #    action='store_false',
    #    dest='header')

    return parser

def csvavg():
    """
    Command line utility to average a csv file
    """
    parser = _default_arguments()
    parser.add_argument('-c', '--cols', nargs='*',
        help='A list of columns. Each column will have an average generated.')
    parser.add_argument('-a', '--alphabetize',
        action='store_true',
        help='A flag to indicate the output should be displayed in ' \
            'alphabetical order. This argument is only valid if the output ' \
            'is transposed. Equivalent to `csvavg ... -T | sort`.')
    parser.add_argument('-p', '--precision',
        type=int,
        help='The number of decimal places to show.')
    parser.add_argument('-t', '--to',
        dest='outformat',
        nargs='?',
        default='csv',
        help='Output file type. Default CSV.')
    parser.add_argument('-T', '--transpose',
        action='store_true',
        help='A flag to indicate the output should be transposed so that ' \
            'there are two columns and N rows, where N equals the number ' \
            'of columns indicated to average.')

    args, remainder = parser.parse_known_args()

    informat = getattr(parsers, args.informat)(designation='inparser')
    outformat = getattr(parsers, args.outformat)(designation='outparser')

    informat.parse_args(remainder)
    outformat.parse_args(remainder)

    cols, avgs = zip(*csvutils.fmap(informat.file, helpers.avg,
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

def csvconvert():
    """
    Command line utility to convert one tabular format to another
    """
    parser = _default_arguments()
    parser.add_argument('-t', '--to',
        dest='outformat',
        nargs='?',
        default='csv',
        help='Output file type. Default CSV.')

    args, remainder = parser.parse_known_args()

    informat = getattr(parsers, args.informat)(designation='inparser')
    outformat = getattr(parsers, args.outformat)(designation='outparser')

    informat.parse_args(remainder)
    outformat.parse_args(remainder)

    csvutils.convert(informat.file, informat, outformat).write(outformat.file)

def csvdrop():
    """
    Command line utility to drop columns from a csv file
    """
    parser = _default_arguments()
    parser.add_argument('-c', '--cols', nargs='*',
        help='A list of columns. Each column listed will be dropped.')

    args, remainder = parser.parse_known_args()

    informat = getattr(parsers, args.informat)(designation='inparser')
    informat.parse_args(remainder)

    header, rows = csvutils.drop(informat.file,
        parser=informat,
        columns=args.cols)

    informat.header = header
    informat.rows = rows
    informat.designation = 'outparser'
    informat.parse_args(remainder)
    informat.write(informat.file)

def csvkeep():
    """
    Command line utiltiy to keep columns in a csv file. The inverse of csvdrop
    """
    parser = _default_arguments()
    parser.add_argument('-c', '--cols', nargs='*',
        help='A list of columns. Each column listed will be kept.')

    args, remainder = parser.parse_known_args()

    informat = getattr(parsers, args.informat)(designation='inparser')
    informat.parse_args(remainder)

    header, rows = csvutils.keep(informat.file,
        parser=informat,
        columns=args.cols)

    informat.header = header
    informat.rows = rows
    informat.designation = 'outparser'
    informat.parse_args(remainder)
    informat.write(informat.file)

def csvsql():
    """
    Command line utility to load csv files into tables in a database
    """
    parser = _default_arguments(infiles='*')
    parser.add_argument('-c', '--command')
    parser.add_argument('-n', '--database-name',
        nargs='?',
        default=':memory:')

    args = parser.parse_args()
    query = args.command

    conn = csvutils.sql(args.infile, args.database_name,
        head=args.header,
        delimiter=args.delim.decode('string-escape'))

    cur = conn.cursor()
    cur.execute(query)

    header = [x[0] for x in cur.description]
    rows = cur.fetchall()

    helpers.writecsv(args.outfile, header, rows)

def csvsum():
    """
    Command line utility to sum a csv file
    """
    parser = _default_arguments()
    parser.add_argument('-c', '--cols', nargs='*',
        help='A list of columns. Each column will have a sum generated.')
    parser.add_argument('-a', '--alphabetize',
        action='store_true',
        help='A flag to indicate the output should be displayed in ' \
            'alphabetical order. This argument is only valid if the output ' \
            'is transposed. Equivalent to `csvsum ... -T | sort`.')
    parser.add_argument('-p', '--precision',
        type=int,
        help='The number of decimal places to show.')
    parser.add_argument('-t', '--to',
        dest='outformat',
        nargs='?',
        default='csv',
        help='Output file type. Default CSV.')
    parser.add_argument('-T', '--transpose',
        action='store_true',
        help='A flag to indicate the output should be transposed so that ' \
            'there are two columns and N rows, where N equals the number ' \
            'of columns indicated to sum.')

    args, remainder = parser.parse_known_args()

    informat = getattr(parsers, args.informat)(designation='inparser')
    outformat = getattr(parsers, args.outformat)(designation='outparser')

    informat.parse_args(remainder)
    outformat.parse_args(remainder)

    cols, sums = zip(*csvutils.fmap(informat.file, sum,
        parser=informat,
        columns=args.cols))

    if args.precision:
        sums = ['{:.{}f}'.format(x, args.precision) for x in sums]

    if args.transpose is True:
        if args.alphabetize is True:
            outformat.rows = sorted(zip(cols, sums), key=lambda x: x[0])
        else:
            outformat.rows = zip(cols, sums)
    else:
        outformat.header = cols
        outformat.rows = [sums]

    outformat.write(outformat.file)

def csvtab():
    """
    Command line utility to tabulate a csv file for easy viewing
    """
    parser = _default_arguments()

    args, remainder = parser.parse_known_args()

    informat = getattr(parsers, args.informat)(designation='inparser')
    outformat = parsers.table()

    informat.parse_args(remainder)
    outformat.parse_args(remainder)

    outformat.rows = csvutils.tabulate(informat.file,
        parser=informat,
        maxw=outformat.column_maxwidth,
        pad=outformat.padding)

    outformat.write(outformat.file)


class CSVUtilsHelpAction(argparse.Action):

    def __call__(self, parser, namespace, value, option_string):
        if value is None:
            parser.print_help()
        else:
            fileparser = getattr(parsers, value)()
            fileparser._inparser.print_help()
            fileparser._outparser.print_help()

        parser.exit()
