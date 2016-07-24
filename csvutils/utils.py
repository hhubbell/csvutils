#
# This file contains the following functionality for csvutils
#   Constants
#   File IO utilities
#   Iterable manipulation
#

import csv


KEY_VALUE_STR_FORMAT = '{:<{}}{:>{}}'


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
    Return the indexed of the needles in the haystack
    :param haystack:    List to search
    :param needles:     Items to find
    :return list:       List of indexes matching needles in haystack
    """
    if needles:
        indexes = [haystack.index(x) for x in needles]
    else:
        indexes = range(len(haystack))

    return indexes

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

def write(fileobj, header, rows):
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
