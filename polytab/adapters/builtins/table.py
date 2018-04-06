#
# table.py
#

from __future__ import absolute_import
from ..base import Adapter


class TableAdapter(Adapter):

    def __init__(self, *args, **kwargs):
        """
        :option delimiter [str]: Column delimiter
        :option lineterminator [str]: Row delimiter
        """
        super(TableAdapter, self).__init__(*args, **kwargs)

        self.designation = 'outparser'
        self.delimiter = kwargs.get('delimiter', ' ')
        self.hasheader = kwargs.get('hasheader', True)
        self.lineterminator = kwargs.get('lineterminator', '\n')
        self.column_maxwidth = kwargs.get('column_maxwidth')
        self.padding = kwargs.get('padding', 0)

    def _set_argparser_options(self):
        """
        Creates an ArgumentParser with the adapter's allowed arguments.
        """
        super(TableAdapter, self)._set_argparser_options()

        self._outparser.add_argument('-D', '--outfile-delim',
            nargs='?',
            default=' ',
            dest='delimiter',
            help='Output delimiter. Default space')
        self._outparser.add_argument('--outfile-no-header',
            action='store_false',
            dest='hasheader',
            help='A flag to indicate the output does not have a header ' \
                'that should be displayed.')
        self._outparser.add_argument('--outfile-lineterminator',
            nargs='?',
            default='\n',
            dest='lineterminator',
            help='Output line terminator. Default newline character.')
        self._outparser.add_argument('--outfile-column-maxwidth',
            type=int,
            dest='column_maxwidth',
            help='The max width of a column. Values that have a width ' \
                'exceeding this number will be truncated.')
        self._outparser.add_argument('--outfile-padding',
            nargs='?',
            type=int,
            default=0,
            dest='padding',
            help='The amount of padding to apply to a column (in spaces). ' \
                'Default no padding.')

    def write(self, fileobj):
        """
        Dump table to an open file handle
        :param fileobj [File]: File object to write to
        """
        try:
            if self.hasheader is True and self.header is not None:
                fileobj.write(self.delimiter.join(self.header) + self.lineterminator)

            for row in self.rows:
                fileobj.write(self.delimiter.join(row) + self.lineterminator)

        except IOError:
            fileobj.close()

