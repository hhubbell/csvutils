

from __future__ import absolute_import
from .base import Parser
import csv


class csv(Parser):

    def read(self, fileobj, header=True, delimiter=','):
        """
        Open a csv file and read it.
        :param fileobj:     Open file object
        :option header:     Use first row in csv file as header row
        :option delimiter:  Column delimiter
        :return tuple:      header, rows tuple
        """
        reader = csv.reader(fileobj, delimiter=delimiter)
        head = next(reader) if header is True else None
        rows = list(reader)
    
        if head is None:
            head = self._generic_header(len(rows[0]))

        self.header = head
        self.rows = rows

        return head, rows

    def write(self, fileobj, header=True, delimiter=','):
        """
        Dump a csv to file object
        :param fileobj:     File object to write to
        :option header:     Write the header row
        :option delimiter:  Column delimiter
        """
        try:
            writer = csv.writer(fileobj, delimiter=delimiter, lineterminator='\n')
            
            if header is True:
                writer.writerow(self.header)

            writer.writerows(self.rows)

        except IOError:
            fileobj.close()
