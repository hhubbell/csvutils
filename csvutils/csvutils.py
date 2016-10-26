#
# CSV Manipulation Library
#

from __future__ import absolute_import
from . import helpers


def col_apply(file_obj, func, columns=None, head=True, delimiter=','):
    """
    Apply a function on given csv columns
    :param file_obj:    Open csv file handle
    :param func:        Function to apply
    :option columns:    CSV header columns to average, default all
    :option head:       Boolean if csv has header row
    :option delimiter:  Column delimiter
    :return list:       List of column: result tuples
    """
    columns = columns if columns is not None else []
    header, rows = helpers.read(file_obj, header=head, delimiter=delimiter)

    if header is None:
        header = helpers.generic_header(len(rows[0]))

    to_app = helpers.indexes(header, columns)
    res = []

    for index in to_app:
        res.append(func(helpers.tofloat(x[index]) for x in rows))

    return zip(helpers.ikeep(header, to_app), res)

def drop(file_obj, columns=None, head=True, delimiter=','):
    """
    Transform a list of headers and rows to remove specific values
    :param file_obj:    Open csv file handle
    :option columns:    CSV header columns to drop, default all
    :option head:       Boolean if csv has header row
    :option delimiter:  Column delimiter
    :return tuple:      New header/rows
    """
    columns = columns if columns is not None else []
    header, rows = helpers.read(file_obj, header=head, delimiter=delimiter)

    if header is None:
        header = helpers.generic_header(len(rows[0]))

    drops = helpers.indexes(header, columns)

    mod_h = helpers.imask(header, drops)
    mod_r = [helpers.imask(x, drops) for x in rows]

    return mod_h, mod_r

def keep(file_obj, columns=None, head=True, delimiter=','):
    """
    Transform a list of headers and rows to keep specific values
    :param file_obj:    Open csv file handle
    :option columns:    CSV header columns to keep, default all
    :option head:       Boolean if csv has header row
    :option delimiter:  Column delimiter
    :return tuple:      New header/rows
    """
    columns = columns if columns is not None else []
    header, rows = helpers.read(file_obj, header=head, delimiter=delimiter)

    if header is None:
        header = helpers.generic_header(len(rows[0]))

    keeps = helpers.indexes(header, columns)

    mod_h = helpers.ikeep(header, keeps)
    mod_r = [helpers.ikeep(x, keeps) for x in rows]

    return mod_h, mod_r

def html(file_obj, pretty=None, head=True, display_header=True, delimiter=','):
    """
    Transform a list of headers and a list of rows into an html table
    :param file_obj:        Open csv file handle
    :option pretty:         True makes html readable
    :option head:           Boolean if csv has header row
    :option display_header: Include <th>..</th>
    :option delimiter:      Column delimiter
    :return str:            HTML string
    """
    TABLE = '<table>\n{}{}\n</table>\n'

    has_header = head and display_header

    header, rows = helpers.read(file_obj, header=has_header, delimiter=delimiter)

    if header is None and head is False:
        header = helpers.generic_header(len(rows[0]))

    h = helpers.makehtmlrow(header, header=True, tabs=pretty) + '\n' if header else ''
    r = (helpers.makehtmlrow(x, tabs=pretty) for x in rows)

    return TABLE.format(h, '\n'.join(r))

def json(file_obj, head=True, delimiter=','):
    """
    Transform a list of headers and a list of rows into a json object
    :param file_obj:    Open csv file handle
    :option head:       Boolean if csv has header row
    :option delimiter:  Column delimiter
    :return list:       Serializable list of dicts
    """
    header, rows = helpers.read(file_obj, header=head, delimiter=delimiter)

    if header is None:
        header = helpers.generic_header(len(rows[0]))

    return [{k: v for k, v in zip(header, row)} for row in rows]

def tabulate(file_obj, maxw=None, pad=0, delimiter=','):
    """
    Format the table
    :param file_obj:    Open csv file handle
    :option maxw:       Max cell width
    :option pad:        Cell padding
    :option delimiter:  Column delimiter
    :return list:       Formatted table in matrix like form.
    """
    header, rows = helpers.read(file_obj, delimiter=delimiter)

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

    return (' '.join(x) for x in zip(*fmtcol))
