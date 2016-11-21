#
# CSV Manipulation Library
#

from __future__ import absolute_import
from . import helpers, parsers


def convert(fileobj, informat, outformat):
    """
    Convert a file from one format to another.
    :param fileobj:         Open tabular file handle
    :param informat:        Parser object for importing file
    :param outformat:       Parser object for exporting file
    """
    header, rows = informat.read(fileobj)
    outformat.header = header
    outformat.rows = rows

    return outformat

def fmap(fileobj, func, parser=None, columns=None):
    """
    Apply a function across columns in a csv file
    :param file_obj:    Open csv file handle
    :param func:        Function to apply
    :option parser:     File parser, will default to standard CSV
    :option columns:    CSV header columns to average, default all
    :return list:       List of column: result tuples
    """
    columns = columns if columns is not None else []
    parser = parser if parser is not None else parsers.csv()

    header, rows = parser.read(fileobj)

    to_app = helpers.indexes(header, columns)
    res = []

    for index in to_app:
        res.append(func(helpers.tofloat(x[index]) for x in rows))

    return zip(helpers.ikeep(header, to_app), res)

def drop(fileobj, parser=None, columns=None):
    """
    Transform a list of headers and rows to remove specific values
    :param file_obj:    Open csv file handle
    :option parser:     File parser, will default to standard CSV
    :option columns:    CSV header columns to drop, default all
    :return tuple:      New header/rows
    """
    columns = columns if columns is not None else []
    parser = parser if parser is not None else parsers.csv()

    header, rows = parser.read(fileobj)

    drops = helpers.indexes(header, columns)

    mod_h = helpers.imask(header, drops)
    mod_r = [helpers.imask(x, drops) for x in rows]

    return mod_h, mod_r

def keep(fileobj, parser=None, columns=None):
    """
    Transform a list of headers and rows to keep specific values
    :param file_obj:    Open csv file handle
    :option parser:     File parser, will default to standard CSV
    :option columns:    CSV header columns to keep, default all
    :return tuple:      New header/rows
    """
    columns = columns if columns is not None else []
    parser = parser if parser is not None else parsers.csv()

    header, rows = parser.read(fileobj)

    keeps = helpers.indexes(header, columns)

    mod_h = helpers.ikeep(header, keeps)
    mod_r = [helpers.ikeep(x, keeps) for x in rows]

    return mod_h, mod_r

def tabulate(fileobj, parser=None, maxw=None, pad=0):
    """
    Format the table
    :param file_obj:    Open csv file handle
    :param parser:      File parser, will default to standard CSV
    :option maxw:       Max cell width
    :option pad:        Cell padding
    :return list:       Formatted table in matrix like form.
    """
    parser = parser if parser is not None else parsers.csv()
    header, rows = parser.read(fileobj)

    full = list(rows)
    full.insert(0, header)
    flat = zip(*full)
    fmt = lambda s, w, a='<': '{:{}{}}'.format(s, a, w)
    fmtcol = []

    for head, vals in zip(header, flat):
        calign = helpers.align(vals[1:])
        cmax = max(len(x) for x in vals) + pad
        cmax = maxw if maxw is not None and maxw < cmax else cmax
        fmtcol.append([fmt(helpers.trunc(x, cmax), cmax, calign) for x in vals])

    return zip(*fmtcol)
