

from __future__ import absolute_import
from ..base import Parser
import csv


class CSVParser(Parser):

    def __init__(self, *args, **kwargs):
        """
        :option delimiter [str]: Column delimiter
        :option hasheader [bool]: Use first row in csv file as header row
        :option lineterminator [str]: Row delimiter
        :option quoting [int]: Quoting level
        """
        super(CSVParser, self).__init__(*args, **kwargs)

        self.delimiter = kwargs.get('delimiter', ',') or ','
        self.hasheader = kwargs.get('hasheader', True)
        self.lineterminator = kwargs.get('lineterminator', '\n')
        self.quoting = kwargs.get('quoting', csv.QUOTE_MINIMAL)

    def read(self, fileobj):
        """
        Open a csv file and read it.
        :param fileobj [File]: Open file object
        :return [tuple]: header, rows tuple
        """
        reader = csv.reader(fileobj, delimiter=self.delimiter)
        head = next(reader) if self.hasheader is True else None
        rows = list(reader)
    
        if head is None:
            head = self._generic_header(len(rows[0]))

        self.header = head
        self.rows = rows

        return head, rows

    def write(self, fileobj):
        """
        Dump a csv to an open file handle
        :param fileobj [File]: File object to write to
        """
        try:
            writer = csv.writer(fileobj,
                delimiter=self.delimiter,
                lineterminator=self.lineterminator,
                quoting=self.quoting)
            
            if self.header is not None:
                writer.writerow(self.header)

            writer.writerows(self.rows)

        except IOError:
            fileobj.close()
