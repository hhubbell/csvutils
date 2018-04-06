#
# Tabular data manipulation library
#

from __future__ import absolute_import
from . import helpers, parsers
import statistics


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

def fmap(fileobj, func, adapter=None, columns=None):
    """
    Apply a function across columns in a csv file
    :param file_obj:    Open csv file handle
    :param func:        Function to apply
    :option adapter:    File adapter, will default to standard CSV
    :option columns:    CSV header columns to average, default all
    :return list:       List of column: result tuples
    """
    columns = columns if columns is not None else []
    adapter = adapter if adapter is not None else adapters.csv()

    header, rows = adapter.read(fileobj)

    to_app = helpers.indexes(header, columns)
    res = []

    for index in to_app:
        res.append(func(helpers.tofloat(x[index]) for x in rows))

    return zip(helpers.ikeep(header, to_app), res)

def drop(fileobj, adapter=None, columns=None):
    """
    Transform a list of headers and rows to remove specific values
    :param file_obj:    Open csv file handle
    :option adapter:    File adapter, will default to standard CSV
    :option columns:    CSV header columns to drop, default all
    :return tuple:      New header/rows
    """
    columns = columns if columns is not None else []
    adapter = adapter if adapter is not None else adapters.csv()

    header, rows = adapter.read(fileobj)

    drops = helpers.indexes(header, columns)

    mod_h = helpers.imask(header, drops)
    mod_r = [helpers.imask(x, drops) for x in rows]

    return mod_h, mod_r

def keep(fileobj, adapter=None, columns=None):
    """
    Transform a list of headers and rows to keep specific values
    :param file_obj:    Open csv file handle
    :option adapter:    File adapter, will default to standard CSV
    :option columns:    CSV header columns to keep, default all
    :return tuple:      New header/rows
    """
    columns = columns if columns is not None else []
    adapter = adapter if adapter is not None else adapters.csv()

    header, rows = adapter.read(fileobj)

    keeps = helpers.indexes(header, columns)

    mod_h = helpers.ikeep(header, keeps)
    mod_r = [helpers.ikeep(x, keeps) for x in rows]

    return mod_h, mod_r

def summarize(fileobj, adapter=None):
    """
    Summarize a table
    :param fileobj: Open file handle
    :option adapter: File adapter, will default to CSV
    :return tuple: New header/rows
    """
    _h, r_mean = fmap(fileobj, statistics.mean, adapter=adapter)
    _h, r_mode = fmap(fileobj, statistics.mode, adapter=adapter)
    _h, r_med = fmap(fileobj, statistics.median, adapter=adapter)
    _h, r_sum = fmap(fileobj, sum, adapter=adapter)

    header = ['attribute'] + _h
    rows = [r_mean, r_mode, r_med, r_sum]

    return header, rows

def tabulate(fileobj, adapter=None, maxw=None, pad=0):
    """
    Format the table
    :param file_obj:    Open csv file handle
    :param adapter:     File adapter, will default to standard CSV
    :option maxw:       Max cell width
    :option pad:        Cell padding
    :return list:       Formatted table in matrix like form.
    """
    adapter = adapter if adapter is not None else adapters.csv('inadapter')
    header, rows = adapter.read(fileobj)

    full = list(rows)
    full.insert(0, header)
    flat = zip(*full)
    fmt = lambda s, w, a='<': '{:{}{}}'.format(s, a, w)
    strnone = lambda x: str(x) if x is not None else None
    fmtcol = []

    for head, vals in zip(header, flat):
        vals = [strnone(x) for x in vals]
        calign = helpers.align(vals[1:])
        cells = [len(x) for x in vals if x is not None]
        cmax = max(cells) + pad if cells else 0
        cmax = maxw if maxw is not None and maxw < cmax else cmax
        fmtcol.append([fmt(helpers.trunc(x, cmax), cmax, calign) for x in vals])

    return zip(*fmtcol)
