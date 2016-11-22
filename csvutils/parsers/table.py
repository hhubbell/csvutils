from __future__ import absolute_import
from .base import Parser


class TableParser(Parser):

    def __init__(self, *args, **kwargs):
        super(TableParser, self).__init__(*args, **kwargs)

        self.delimiter = kwargs.get('delimiter', ' ') or ' '
        self.lineterminator = kwargs.get('lineterminator', '\n')

    def write(self, fileobj):
        """
        Dump an iterable to file object
        :param fileobj:     File object to write to
        """
        try:
            if self.header is not None:
                fileobj.write(self.delimiter.join(self.header) + self.lineterminator)

            for row in self.rows:
                fileobj.write(self.delimiter.join(row) + self.lineterminator)

        except IOError:
            fileobj.close()

