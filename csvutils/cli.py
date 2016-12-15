#
# Provide a consistent argparser api
#

from __future__ import absolute_import
from . import csvutils, helpers, parsers
import argparse
import csv
import pkg_resources
import sys


def _default_arguments():
    """
    Returns ArgumentParser with args used in all utils
    :return ArgumentParser:     ArgumentParser object
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--from',
        dest='informat',
        nargs='?',
        default='csv',
        help='Input file type. Default CSV.')
    parser.add_argument('-v', '--version',
        action='version',
        version=pkg_resources.get_distribution(__package__).version,
        help='Print version number and quit')
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
    parser.add_argument('-c', '--cols', nargs='*')
    parser.add_argument('-a', '--alphabetize',
        action='store_true')
    parser.add_argument('-p', '--precision',
        type=int)
    parser.add_argument('-t', '--to',
        dest='outformat',
        nargs='?',
        default='csv')
    parser.add_argument('-T', '--transpose',
        action='store_true')

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
        default='csv')

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
    parser.add_argument('-c', '--cols', nargs='*')

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
    parser.add_argument('-c', '--cols', nargs='*')

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

def csvsum():
    """
    Command line utility to sum a csv file
    """
    parser = _default_arguments()
    parser.add_argument('-c', '--cols', nargs='*')
    parser.add_argument('-a', '--alphabetize',
        action='store_true')
    parser.add_argument('-p', '--precision',
        type=int)
    parser.add_argument('-t', '--to',
        dest='outformat',
        nargs='?',
        default='csv')
    parser.add_argument('-T', '--transpose',
        action='store_true')

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
