#
# csv.py
#

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

        self.delimiter = kwargs.get('delimiter',
            getattr(self, 'delimiter', ','))
        self.infile_hasheader = kwargs.get('hasheader',
            getattr(self, 'hasheader', True))
        self.infile_lineterminator = kwargs.get('lineterminator',
            getattr(self, 'lineterminator', '\n'))
        self.quoting = kwargs.get('quoting',
            getattr(self, 'quoting', csv.QUOTE_MINIMAL))

    def _set_argparser_options(self):
        """
        Creates an ArgumentParser with the parser's allowed arguments.
        """
        super(CSVParser, self)._set_argparser_options()

        self._inparser.add_argument('-d', '--infile-delim',
            nargs='?',
            default=',',
            dest='delimiter')
        self._inparser.add_argument('--infile-no-header',
            action='store_false',
            dest='hasheader')
        self._inparser.add_argument('--infile-lineterminator',
            nargs='?',
            default='\n',
            dest='lineterminator')
        self._inparser.add_argument('--infile-quoting',
            nargs='?',
            default=csv.QUOTE_MINIMAL,
            dest='quoting',
            choices=[csv.QUOTE_ALL,
                csv.QUOTE_MINIMAL,
                csv.QUOTE_NONNUMERIC,
                csv.QUOTE_NONE])

        self._outparser.add_argument('-D', '--outfile-delim',
            nargs='?',
            default=',',
            dest='delimiter')
        self._outparser.add_argument('--outfile-no-header',
            action='store_false',
            dest='hasheader')
        self._outparser.add_argument('--outfile-lineterminator',
            nargs='?',
            default='\n',
            dest='lineterminator')
        self._outparser.add_argument('--outfile-quoting',
            nargs='?',
            default=csv.QUOTE_MINIMAL,
            dest='quoting',
            choices=[csv.QUOTE_ALL,
                csv.QUOTE_MINIMAL,
                csv.QUOTE_NONNUMERIC,
                csv.QUOTE_NONE])

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
