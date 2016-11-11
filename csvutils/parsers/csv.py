

from __future__ import absolute_import
from .base import Parser
import csv


class CSVParser(Parser):

    def __init__(self, *args, **kwargs):
        """
        """
        super(CSVParser, self).__init__(*args, **kwargs)

        self.delimiter = kwargs.get('delimiter', ',')
        self.hasheader = kwargs.get('hasheader', True)

    def read(self, fileobj):
        """
        Open a csv file and read it.
        :param fileobj:     Open file object
        :option header:     Use first row in csv file as header row
        :option delimiter:  Column delimiter
        :return tuple:      header, rows tuple
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
        Dump a csv to file object
        :param fileobj:     File object to write to
        """
        try:
            writer = csv.writer(fileobj, delimiter=self.delimiter, lineterminator='\n')
            
            if self.header is not None:
                writer.writerow(self.header)

            writer.writerows(self.rows)

        except IOError:
            fileobj.close()
