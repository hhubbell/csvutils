#
# Provide a consistent argparser api
#

from __future__ import absolute_import
from . import csvutils, helpers, parsers
import argparse
import csv
import sys

def _default_arguments():
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
    parser.add_argument('-f', '--from',
        dest='informat',
        nargs='?',
        default='csv')
    parser.add_argument('-N', '--no-header',
        action='store_false',
        dest='header')
    parser.add_argument('-o', '--outfile',
        nargs='?',
        type=argparse.FileType('w'),
        default=sys.stdout)

    return parser

def csvavg():
    """
    Command line utility to average a csv file
    """
    parser = _default_arguments()
    parser.add_argument('cols', nargs=argparse.REMAINDER)
    parser.add_argument('-a', '--alphabetize',
        action='store_true')
    parser.add_argument('-D', '--outfile-delim',
        nargs='?',
        default=': ')
    parser.add_argument('-p', '--precision',
        type=int)
    parser.add_argument('-t', '--tabulate',
        action='store_true')

    args = parser.parse_args()
    seper = args.outfile_delim

    cols, avgs = zip(*csvutils.fmap(args.infile, helpers.avg,
        columns=args.cols,
        head=args.header,
        delimiter=args.delim))

    if args.precision:
        avgs = ['{:.{}f}'.format(x, args.precision) for x in avgs]

    if args.tabulate is True:
        hwidth = max(len(x) for x in cols) + len(seper)
        rwidth = max(len(str(x)) for x in avgs)
    else:
        hwidth = ''
        rwidth = ''

    if args.alphabetize is True:
        zipped = sorted(zip(cols, avgs), key=lambda x: args.header[x[0]])
    else:
        zipped = zip(cols, avgs)

    for column, value in zipped:
        key = column + seper
        line = helpers.KEY_VALUE_STR_FORMAT.format(key, hwidth, value, rwidth)

        helpers.write(args.outfile, line)

def csvconvert():
    """
    Command line utility to convert one tabular format to another
    """
    parser = _default_arguments()
    parser.add_argument('-D', '--outfile-delim',
        nargs='?',
        default=',')
    parser.add_argument('-p', '--pretty',
        action='store_true')
    parser.add_argument('-t', '--to',
        dest='outformat',
        nargs='?',
        default='csv')

    args = parser.parse_args()

    informat = getattr(parsers, args.informat)(
        delimiter=args.delim,
        hasheader=args.header)
    outformat = getattr(parsers, args.outformat)(
        delimiter=args.outfile_delim,
        pretty=args.pretty)

    csvutils.convert(args.infile, informat, outformat).write(args.outfile)

def csvdrop():
    """
    Command line utility to drop columns from a csv file
    """
    parser = _default_arguments()
    parser.add_argument('cols', nargs='+')

    args = parser.parse_args()

    informat = getattr(parsers, args.informat)(
        delimiter=args.delim,
        hasheader=args.header)

    header, rows = csvutils.drop(args.infile,
        parser=informat,
        columns=args.cols)

    informat.header = header
    informat.rows = rows
    informat.write(args.outfile)

def csvkeep():
    """
    Command line utiltiy to keep columns in a csv file. The inverse of csvdrop
    """
    parser = _default_arguments()
    parser.add_argument('cols', nargs='+')

    args = parser.parse_args()

    informat = getattr(parsers, args.informat)(
        delimiter=args.delim,
        hasheader=args.header)

    header, rows = csvutils.keep(args.infile,
        parser=informat,
        columns=args.cols)

    informat.header = header
    informat.rows = rows
    informat.write(args.outfile)

def csvsum():
    """
    Command line utility to sum a csv file
    """
    parser = _default_arguments()
    parser.add_argument('cols', nargs=argparse.REMAINDER)
    parser.add_argument('-a', '--alphabetize',
        action='store_true')
    parser.add_argument('-D', '--outfile-delim',
        nargs='?',
        default=': ')
    parser.add_argument('-p', '--precision',
        type=int)
    parser.add_argument('-t', '--tabulate',
        action='store_true')

    args = parser.parse_args()
    seper = args.outfile_delim

    cols, sums = zip(*csvutils.fmap(args.infile, sum,
        columns=args.cols,
        head=args.header,
        delimiter=args.delim))

    if args.precision:
        sums = ['{:.{}f}'.format(x, args.precision) for x in sums]

    if args.tabulate is True:
        hwidth = max(len(x) for x in cols) + len(seper)
        rwidth = max(len(str(x)) for x in sums)
    else:
        hwidth = ''
        rwidth = ''

    if args.alphabetize is True:
        zipped = sorted(zip(cols, sums), key=lambda x: args.header[x[0]])
    else:
        zipped = zip(cols, sums)

    for column, value in zipped:
        key = column + seper
        line = helpers.KEY_VALUE_STR_FORMAT.format(key, hwidth, value, rwidth)

        helpers.write(args.outfile, line)

def csvtab():
    """
    Command line utility to tabulate a csv file for easy viewing
    """
    parser = _default_arguments()
    parser.add_argument('-m', '--maxlength',
        type=int)
    parser.add_argument('-p', '--padding',
        nargs='?',
        type=int,
        default=0)

    args = parser.parse_args()

    informat = getattr(parsers, args.informat)(
        delimiter=args.delim,
        hasheader=args.header)
    outformat = parsers.table()

    outformat.rows = csvutils.tabulate(args.infile,
        parser=informat,
        maxw=args.maxlength,
        pad=args.padding)

    outformat.write(args.outfile)
