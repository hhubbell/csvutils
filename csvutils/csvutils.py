#
# CSV Manipulation Library
#

from __future__ import absolute_import
from . import helpers


def col_apply(header, rows, func, columns=None):
    """
    Apply a function on given csv columns
    :param header:      CSV header
    :param rows:        CSV rows
    :param func:        Function to apply
    :option columns:    CSV header columns to average, default all
    :return list:       List of column: result tuples
    """
    columns = columns if columns is not None else []
    to_app = helpers.indexes(header, columns)
    res = []

    for index in to_app:
        res.append(func(helpers.tofloat(x[index]) for x in rows))

    return zip(helpers.ikeep(header, to_app), res)

def drop(header, rows, columns=None):
    """
    Transform a list of headers and rows to remove specific values
    :param header:      CSV header
    :param rows:        CSV rows
    :option columns:    CSV header columns to drop, default all
    :return tuple:      New header/rows
    """
    columns = columns if columns is not None else []
    drops = helpers.indexes(header, columns)

    mod_h = helpers.imask(header, drops)
    mod_r = [helpers.imask(x, drops) for x in rows]

    return mod_h, mod_r

def keep(header, rows, columns=None):
    """
    Transform a list of headers and rows to keep specific values
    :param header:      CSV header
    :param rows:        CSV rows
    :option columns:    CSV header columns to keep, default all
    :return tuple:      New header/rows
    """
    columns = columns if columns is not None else []
    drops = helpers.indexes(header, columns)

    mod_h = helpers.ikeep(header, drops)
    mod_r = [helpers.ikeep(x, drops) for x in rows]

    return mod_h, mod_r

def html(header, rows, pretty=None):
    """
    Transform a list of headers and a list of rows into an html table
    :param header:      csv header
    :param rows:        csv rows
    :option pretty:     True makes html readable
    :return str:        HTML string
    """
    TABLE = '<table>\n{}{}\n</table>\n'

    h = helpers.makehtmlrow(header, header=True, tabs=pretty) + '\n' if header else ''
    r = (helpers.makehtmlrow(x, tabs=pretty) for x in rows)

    return TABLE.format(h, '\n'.join(r))

def json(header, rows):
    """
    Transform a list of headers and a list of rows into a json object
    :param header:      CSV header
    :param rows:        CSV rows
    :return lsit:       Serializable list of dicts
    """
    return [{k: v for k, v in zip(header, row)} for row in rows]

def tabulate(header, rows, maxw=None, pad=0):
    """
    Format the table
    :param header:      Table header
    :param rows:        Table rows
    :option maxw:       Max cell width
    :option pad:        Cell padding
    :return list:       Formatted table in matrix like form.
    """
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

    return '\n'.join(' '.join(x) for x in zip(*fmtcol))
