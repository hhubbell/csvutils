#
# Provide a consistent argparser api
#

from __future__ import absolute_import
from . import csvutils, helpers
import argparse
import json
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
    parser.add_argument('-N', '--no-header',
        action='store_false',
        dest='header')
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

    delim = args.delim.decode('string-escape')
    seper = args.outfile_delim.decode('string-escape')

    header, rows = helpers.read(args.infile, header=args.header, delimiter=delim)

    if header is None:
        header = helpers.generic_header(len(rows[0]))

    cols, avgs = zip(*csvutils.col_apply(header, rows, helpers.avg, args.cols))

    if args.precision:
        avgs = ['{:.{}f}'.format(x, args.precision) for x in avgs]

    if args.tabulate is True:
        hwidth = max(len(x) for x in cols) + len(seper)
        rwidth = max(len(str(x)) for x in avgs)
    else:
        hwidth = ''
        rwidth = ''

    if args.alphabetize is True:
        zipped = sorted(zip(cols, avgs), key=lambda x: header[x[0]])
    else:
        zipped = zip(cols, avgs)

    for column, value in zipped:
        key = column + seper
        print(helpers.KEY_VALUE_STR_FORMAT.format(key, hwidth, value, rwidth))

def csvdrop():
    """
    Command line utiltiy to drop columns from a csv file
    """
    parser = _default_arguments()
    parser.add_argument('cols', nargs='+')

    args = parser.parse_args()

    outfile = sys.stdout
    delim = args.delim.decode('string-escape')

    header, rows = helpers.read(args.infile, header=args.header, delimiter=delim)

    if header is None:
        header = helpers.generic_header(len(rows[0]))

    helpers.write(outfile, *csvutils.drop(header, rows, args.cols))

def csvkeep():
    """
    Command line utiltiy to keep columns in a csv file. The inverse of csvdrop
    """
    parser = _default_arguments()
    parser.add_argument('cols', nargs='+')

    args = parser.parse_args()

    outfile = sys.stdout
    delim = args.delim.decode('string-escape')

    header, rows = helpers.read(args.infile, header=args.header, delimiter=delim)

    if header is None:
        header = helpers.generic_header(len(rows[0]))

    helpers.write(outfile, *csvutils.keep(header, rows, args.cols))

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

    delim = args.delim.decode('string-escape')
    seper = args.outfile_delim.decode('string-escape')

    header, rows = helpers.read(args.infile, delimiter=delim)

    if header is None:
        header = helpers.generic_header(len(rows[0]))

    cols, sums = zip(*csvutils.col_apply(header, rows, sum, args.cols))

    if args.precision:
        sums = ['{:.{}f}'.format(x, args.precision) for x in sums]

    if args.tabulate is True:
        hwidth = max(len(x) for x in cols) + len(seper)
        rwidth = max(len(str(x)) for x in sums)
    else:
        hwidth = ''
        rwidth = ''

    if args.alphabetize is True:
        zipped = sorted(zip(cols, sums), key=lambda x: header[x[0]])
    else:
        zipped = zip(cols, sums)

    for column, value in zipped:
        key = column + seper
        print(helpers.KEY_VALUE_STR_FORMAT.format(key, hwidth, value, rwidth))

def csvtab():
    """
    Command line utility to tabulate a csv file for easy viewing
    """
    parser = _default_arguments()
    parser.add_argument('-m', '--maxlength',
        type=int)
    parser.add_argument('-p', '--padding',
        type=int)

    args = parser.parse_args()

    outfile = sys.stdout
    padding = args.padding or 0
    delim = args.delim.decode('string-escape')

    header, rows = helpers.read(args.infile, delimiter=delim)

    try:
        outfile.write(csvutils.tabulate(header, rows, args.maxlength, padding))
    except IOError:
        outfile.close()

def csvtohtml():
    """
    Command line utility to transform a csv file to an HTML table
    """
    parser = _default_arguments()
    parser.add_argument('-D', '--no-display-header',
        action='store_false',
        dest='display_header')
    parser.add_argument('-p', '--pretty',
        action='store_true',
        help='Try to make the html human readable')

    args = parser.parse_args()

    infile = args.infile
    outfile = sys.stdout
    header = args.header and args.display_header
    delim = args.delim.decode('string-escape')

    header, rows = helpers.read(infile, header=header, delimiter=delim)

    if header is None and args.header is False:
        header = helpers.generic_header(len(rows[0]))

    try:
        outfile.write(csvutils.html(header, rows, pretty=args.pretty))
    except IOError:
        outfile.close()

def csvtojson():
    """
    Command line utility to transform a csv file into json
    """
    parser = _default_arguments()
    parser.add_argument('-p', '--pretty',
        action='store_true',
        help='Try to make the json human readable')

    args = parser.parse_args()

    infile = args.infile
    outfile = sys.stdout
    delim = args.delim.decode('string-escape')
    tabs = helpers.TAB_WIDTH if args.pretty else None

    header, rows = helpers.read(infile, header=args.header, delimiter=delim)

    if header is None and args.header is False:
        header = helpers.generic_header(len(rows[0]))

    json.dump(csvutils.json(header, rows), outfile, indent=tabs, sort_keys=True)
