#
# Manage types
#

from datetime import datetime
import decimal


def tofloat(value):
    """
    Convert a value to a float.  Return 0 for any failures.
    :param value:       Value to convert
    :return float:      Converted value
    """
    try:
        number = decimal.Decimal(value)
    except decimal.InvalidOperation:
        number = decimal.Decimal(0)

    return number

def cast(value):
    """
    Guess a values type and cast that value to it.
    :param value:   String value to cast
    :return mixed:  New cast value
    """
    # Cast to decimal for now
    return tofloat(value)

def get(value):
    """
    Guess a values type and return that type.
    :param value:   Value to guess type
    :return type:   Value type
    """
    return decimal.Decimal

def get_all(values, indexes=None, strict=True):
    """
    """
    indexes = indexes if indexes is not None else range(len(values))
    types = [get(values[x]) for x in indexes]

    #if strict is False: XXX FIXME

    return types
        

