#
# table.py
#

from __future__ import absolute_import
from ..base import Parser


class TableParser(Parser):

    def __init__(self, *args, **kwargs):
        """
        :option delimiter [str]: Column delimiter
        :option lineterminator [str]: Row delimiter
        """
        super(TableParser, self).__init__(*args, **kwargs)

        self.designation = 'outparser'
        self.delimiter = kwargs.get('delimiter', ' ')
        self.hasheader = kwargs.get('hasheader', True)
        self.lineterminator = kwargs.get('lineterminator', '\n')
        self.column_maxwidth = kwargs.get('column_maxwidth')
        self.padding = kwargs.get('padding', 0)

    def _set_argparser_options(self):
        """
        Creates an ArgumentParser with the parser's allowed arguments.
        """
        super(TableParser, self)._set_argparser_options()

        self._outparser.add_argument('-D', '--outfile-delim',
            nargs='?',
            default=' ',
            dest='delimiter')
        self._outparser.add_argument('--outfile-no-header',
            action='store_false',
            dest='hasheader')
        self._outparser.add_argument('--outfile-lineterminator',
            nargs='?',
            default='\n',
            dest='lineterminator')
        self._outparser.add_argument('--outfile-column-maxwidth',
            type=int,
            dest='column_maxwidth')
        self._outparser.add_argument('--outfile-padding',
            nargs='?',
            type=int,
            default=0,
            dest='padding')

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

