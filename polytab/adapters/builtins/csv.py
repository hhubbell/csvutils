#
# csv.py
#

from __future__ import absolute_import
from ..base import Adapter
from ...common_table import CommonTable
import csv


class CSVAdapter(Adapter):

    def __init__(self, *args, **kwargs):
        """
        :option delimiter [str]: Column delimiter
        :option hasheader [bool]: Use first row in csv file as header row
        :option lineterminator [str]: Row delimiter
        :option quoting [int]: Quoting level
        """
        super(CSVAdapter, self).__init__(*args, **kwargs)

        self.delimiter = kwargs.get('delimiter', ',')
        self.hasheader = kwargs.get('hasheader', True)
        self.lineterminator = kwargs.get('lineterminator', '\n')
        self.quoting = kwargs.get('quoting', csv.QUOTE_MINIMAL)

    def _set_argparser_options(self):
        """
        Creates an ArgumentParser with the adapter's allowed arguments.
        """
        super(CSVAdapter, self)._set_argparser_options()

        self._inparser.add_argument('-d', '--infile-delim',
            nargs='?',
            default=',',
            dest='delimiter',
            help='Input file delimiter. Default comma.')
        self._inparser.add_argument('--infile-no-header',
            action='store_false',
            dest='hasheader',
            help='A flag to indicate the first row of the input file ' \
                'is not the header row. If set, a generic header will be ' \
                'assigned.')
        self._inparser.add_argument('--infile-lineterminator',
            nargs='?',
            default='\n',
            dest='lineterminator',
            help='Input file line terminator. Default newline character.')
        self._inparser.add_argument('--infile-quoting',
            nargs='?',
            default=csv.QUOTE_MINIMAL,
            dest='quoting',
            choices=[csv.QUOTE_ALL,
                csv.QUOTE_MINIMAL,
                csv.QUOTE_NONNUMERIC,
                csv.QUOTE_NONE],
            help='Input file quoting level. Default 0; QUOTE_MINIMAL. ' \
                'Other options are: 1 - QUOTE_ALL\n2 - QUOTE_NONNUMERIC\n' \
                '3 - QUOTE_NONE')

        self._outparser.add_argument('-D', '--outfile-delim',
            nargs='?',
            default=',',
            dest='delimiter',
            help='Output file delimiter. Default comma.')
        self._outparser.add_argument('--outfile-no-header',
            action='store_false',
            dest='hasheader',
            help='A flag to indicate the first row of the output file ' \
                'should not be the header. If set, no header will be output ' \
                'regardless of whether a header exists.')
        self._outparser.add_argument('--outfile-lineterminator',
            nargs='?',
            default='\n',
            dest='lineterminator',
            help='Output file line terminator. Default newline character.')
        self._outparser.add_argument('--outfile-quoting',
            nargs='?',
            default=csv.QUOTE_MINIMAL,
            dest='quoting',
            choices=[csv.QUOTE_ALL,
                csv.QUOTE_MINIMAL,
                csv.QUOTE_NONNUMERIC,
                csv.QUOTE_NONE],
            help='Output file quoting level. Default 0 - QUOTE_MINIMAL. ' \
                'Other options are: 1 - QUOTE_ALL 2 - QUOTE_NONNUMERIC\n' \
                '3 - QUOTE_NONE')

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

        self.data = CommonTable(head, rows)

        return self.data

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
            
            if self.data.header is not None and self.hasheader is not False:
                writer.writerow(self.data.header)

            writer.writerows(self.data.rows)

        except IOError:
            fileobj.close()
