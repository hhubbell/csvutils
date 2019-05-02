#
# table.py
#

from __future__ import absolute_import
from ..base import Writer, AdapterMethodNotSupportedError
from ...common_table import CommonTable


def adapter(method, *args, **kwargs):
    """
    Takes a string adapter method name (`writer`) and returns the appropriate
    adapter class. This method exists primarily to support dynamic arguments
    passed at the command line. Users that want to use a `TableWriter`
    adapter should do so directly. A `reader` argument as no support timeline.
    :param method [str]: Adapter method
    :return [object]: Initialized adapter object
    """
    if method == 'reader':
        # NOTE: TableReader will never be supported because it is a
        # space-delimited output format used for the `tab` method only.
        raise AdapterMethodNotSupportedError(method)
    elif method == 'writer':
        adapt = TableWriter()
    else:
        raise AdapterMethodNotSupportedError(method)

    return adapt


class TableWriter(Writer):

    def __init__(self, *args, **kwargs):
        """
        :option column_maxwidth [int]: Maximum column width
        :option delimiter [str]: Column delimiter
        :option hasheader [bool]: Table has header to display
        :option lineterminator [str]: Row delimiter
        :option padding [int]: Additional padding to apply to each cell
        """
        super(TableWriter, self).__init__(*args, **kwargs)

        self.designation = 'outparser'
        self.column_maxwidth = kwargs.get('column_maxwidth')
        self.delimiter = kwargs.get('delimiter', ' ')
        self.hasheader = kwargs.get('hasheader', True)
        self.lineterminator = kwargs.get('lineterminator', '\n')
        self.padding = kwargs.get('padding', 0)

    def _set_argparser_options(self):
        """
        Creates an ArgumentParser with the adapter's allowed arguments.
        """
        super(TableWriter, self)._set_argparser_options()

        self._parser.add_argument('-D', '--outfile-delim',
            nargs='?',
            default=' ',
            dest='delimiter',
            help='Output delimiter. Default space')
        self._parser.add_argument('--outfile-no-header',
            action='store_false',
            dest='hasheader',
            help='A flag to indicate the output does not have a header ' \
                'that should be displayed.')
        self._parser.add_argument('--outfile-lineterminator',
            nargs='?',
            default='\n',
            dest='lineterminator',
            help='Output line terminator. Default newline character.')
        self._parser.add_argument('--outfile-column-maxwidth',
            type=int,
            dest='column_maxwidth',
            help='The max width of a column. Values that have a width ' \
                'exceeding this number will be truncated.')
        self._parser.add_argument('--outfile-padding',
            nargs='?',
            type=int,
            default=0,
            dest='padding',
            help='The amount of padding to apply to a column (in spaces). ' \
                'Default no padding.')

    def _align(self, values):
        """
        Determine alignment based on column datatype. This can be very slow.
        :param values [itr]: Column values
        :return [str]: str.format microlanguage alignment character
        """
        try:
            [float(x) for x in values if x is not None]
            alg = '>'
        except (ValueError, TypeError):
            alg = '<'

        return alg

    def _trunc(self, string, width, replace='...'):
        """
        Truncate a string if it exceeds the specified width, replacing
        the truncated data with an ellipsis or other.
        :param string [str]: String to truncate
        :param width [int]: Max string length
        :option replace [str]: Replace truncated data with
        :return [str]: New truncated string
        """
        string = '' if string is None else string

        return string[:width - len(replace)] + replace if len(string) > width else string

    def tabulate(self, iterable):
        """
        Format the table.
        :param iterable [itr]: Table like data
        :return [list]: Formatted table in matrix like form.
        """
        maxw = self.column_maxwidth
        pad = self.padding

        fmt = lambda s, w, a='<': '{:{}{}}'.format(s, a, w)
        strnone = lambda x: str(x) if x is not None else None
        fmtcol = []

        for vals in zip(*list(iterable)):
            vals = [strnone(x) for x in vals]
            calign = self._align(vals[1:])
            cells = [len(x) for x in vals if x is not None]
            cmax = max(cells) + pad if cells else 0
            cmax = maxw if maxw is not None and maxw < cmax else cmax
            fmtcol.append([fmt(self._trunc(x, cmax), cmax, calign) for x in vals])

        # FIXME: Return CommonTable
        return zip(*fmtcol)

    def write(self, fileobj):
        """
        Dump table to an open file handle
        :param fileobj [File]: File object open for writing
        """
        try:
            # `self.tabulate()` returns the entire table body, so no need
            # to format a header row (for now)
            for row in self.tabulate(self.data):
                fileobj.write(self.delimiter.join(row) + self.lineterminator)

        except IOError:
            fileobj.close()

