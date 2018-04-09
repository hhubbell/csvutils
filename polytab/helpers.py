#
# File:         helpers.py
# Description:  This file contains the following functionality:
#                   Constants
#                   File IO utilities
#                   Iterable manipulation
#

from __future__ import division
import decimal


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

def tofloat(value):
    """
    Convert a value to a float.  Return 0 for any failures.
    :param value:       Value to convert
    :return float:      Converted value
    """
    value = 0 if value is None else value

    try:
        number = decimal.Decimal(value)
    except (decimal.InvalidOperation, TypeError):
        number = decimal.Decimal(0)

    return number
