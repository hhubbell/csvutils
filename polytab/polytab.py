#
# Tabular data manipulation library
#

from __future__ import absolute_import
from contextlib import contextmanager
from . import helpers, adapters
from .common_table import CommonTable
import statistics


@contextmanager
def coupler(reader, writer):
    """
    Define a coupler pipeline MVP
    """
    writer.data = reader.read(reader.file)
    yield writer

def fmap(fileobj, func, adapter=None, columns=None):
    """
    Apply a function across columns in a csv file
    :param file_obj:    Open csv file handle
    :param func:        Function to apply
    :option adapter:    File adapter, will default to standard CSV
    :option columns:    CSV header columns to average, default all
    :return list:       List of column: result tuples
    """
    data = keep(fileobj, adapter, columns)

    res = []
    for index in range(len(data.header)):
        res.append(func(helpers.tofloat(x[index]) for x in data.rows))

    return CommonTable(data.header, [res])

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

    data = adapter.read(fileobj)

    drops = helpers.indexes(data.header, columns)

    mod_h = helpers.imask(data.header, drops)
    mod_r = [helpers.imask(x, drops) for x in data.rows]

    return CommonTable(mod_h, mod_r)

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

    data = adapter.read(fileobj)

    keeps = helpers.indexes(data.header, columns)

    mod_h = helpers.ikeep(data.header, keeps)
    mod_r = [helpers.ikeep(x, keeps) for x in data.rows]

    return CommonTable(mod_h, mod_r)

def summarize(fileobj, adapter=None):
    """
    Summarize a table
    :param fileobj: Open file handle
    :option adapter: File adapter, will default to CSV
    :return tuple: New header/rows
    """
    adapter = adapter if adapter is not None else adapters.csv()
    
    # FIXME: After fileobj is consumed once, it can't be used again.
    #        This API could use some improvement anyway.
    means = fmap(fileobj, statistics.mean, adapter=adapter)
    #modes = fmap(fileobj, statistics.mode, adapter=adapter)
    medians = fmap(fileobj, statistics.median, adapter=adapter)
    sums = fmap(fileobj, sum, adapter=adapter)

    header = ['attribute'] + means.header
    rows = [
        ['mean'] + means.rows[0],
        #['mode'] + modes.rows,
        ['median'] + medians.rows[0],
        ['sum'] + sums.rows[0]]

    return CommonTable(header, rows)
