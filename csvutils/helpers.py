#
# This file contains the following functionality for csvutils
#   Constants
#   File IO utilities
#   Iterable manipulation
#

from __future__ import division
import csv


KEY_VALUE_STR_FORMAT = '{:<{}}{:>{}}'
TAB_WIDTH = 4


def align(values):
    """
    Determine alignment based on column datatype.
    :param values:      Column values
    :return string:     str.format microlanguage alignment character
    """
    try:
        [float(x) for x in values]
        alg = '>'
    except ValueError:
        alg = '<'

    return alg

def avg(values):
    """
    Return the average of a list of numbers
    :param values:      Iter of values
    :return float:      Average of values
    """
    values = list(values)
    return sum(values) / len(values)

def generic_header(columns):
    """
    Generate a list of generic header columns to use
    if the csv file does not have a header.
    :param columns:     Number of columns to generate
    :return list:       Generic column list
    """
    return ['col{}'.format(x) for x in range(columns)]

def ikeep(vals, indexes):
    """
    Inverse of imask
    :param vals:        List to mask
    :param indexes:     List of indexes to apply
    :return list:       Masked list
    """
    return [x for i, x in enumerate(vals) if i in indexes]

def imask(vals, indexes):
    """
    Mask a list based on a list of indexes
    :param vals:        List to mask
    :param indexes:     List of indexes to apply
    :return list:       Masked list
    """
    return [x for i, x in enumerate(vals) if i not in indexes]

def indexes(haystack, needles):
    """
    Return the indexes of the needles in the haystack
    :param haystack:    List to search
    :param needles:     Items to find
    :return list:       List of indexes matching needles in haystack
    """
    if needles:
        indexes = [haystack.index(x) for x in needles]
    else:
        indexes = range(len(haystack))

    return indexes

def makehtmlrow(row, header=False, tabs=False):
    """
    Format one row of data
    :param row:         Row to format
    :option header:     Header row flag
    :option tabs:       Make html human readable by using \n and \t. Tabs
                        will be TAB_WIDTH
    :return str:        Table row
    """
    tabf = ' ' * TAB_WIDTH if tabs is True else ''
    newl = '\n' if tabs is True else ''
    joiner = '{}{}'.format(newl, tabf * 2)

    col = '<td>{}</td>' if header is False else '<th>{}</th>'
    return '{t}<tr>{j}{col}{n}{t}</tr>'.format(
        col=joiner.join(col.format(x) for x in row),
        j=joiner,
        n=newl,
        t=tabf)

def read(src, header=True, delimiter=','):
    """
    Open a csv file and read it.
    :param src:         File path
    :option header:     Use first row in csv file as header row
    :option delimiter:  Column delimiter
    :return tuple:      header, rows tuple
    """
    reader = csv.reader(src, delimiter=delimiter)
    head = next(reader) if header is True else None

    return head, list(reader)

def tofloat(value):
    """
    Convert a value to a float.  Return 0 for any failures.
    :param value:       Value to convert
    :return float:      Converted value
    """
    try:
        number = float(value)
    except ValueError:
        number = 0.0

    return number

def trunc(string, width, replace='...'):
    """
    Truncate a string if it exceeds the specified width, replacing
    the truncated data with an ellipsis or other.
    :param string:      String to truncate
    :param width:       Max string length
    :option replace:    Replace truncated data with
    :return string:     New truncated string
    """
    return string[:width - len(replace)] + replace if len(string) > width else string

def write(fileobj, string, newline='\n'):
    """
    Dump a string to a file object
    :param fileobj:     File object to write to
    :param string:      String to write
    :option newline:    Line ending
    """
    try:
        fileobj.write(string + newline)
    except IOError:
        fileobj.close()

def writecsv(fileobj, header, rows):
    """
    Dump a csv to file object
    :param fileobj:     File object to write to
    :param header:      csv header
    :param rows:        csv rows
    """
    try:
        writer = csv.writer(fileobj, lineterminator='\n')
        writer.writerow(header)
        writer.writerows(rows)
    except IOError:
        fileobj.close()
