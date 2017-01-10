#
# xlsx parser
#

from __future__ import absolute_import
from ..base import Parser
import datetime
import functools
import zipfile
import xml.etree.ElementTree as ElementTree


def nstag(ns, tag):
    return '{{{}}}{}'.format(ns, tag)


class XLSXParser(Parser):
    READ_MODE = 'rb'
    WRITE_MODE = 'wb'

    NS_MAIN = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'

    STRINGS = 'xl/sharedStrings.xml'
    WORKBOOK = 'xl/workbook.xml'
    WORKSHEET = 'xl/worksheets/sheet{}.xml'

    EPOCH = datetime.date(1900, 1, 1)

    def __init__(self, *args, **kwargs):
        """
        :option sheet_name [str]: Target sheet
        :option dimension [str]: Excel range notation (A1:B2)
        :option hasheader [bool]: Use first row in table as header
        """
        super(XLSXParser, self).__init__(*args, **kwargs)

        self.sheet_name = kwargs.get('sheet_name', 'Sheet1')
        self.dimension = kwargs.get('dimension')
        self.hasheader = kwargs.get('hasheader', True)

    def _col_to_num(self, column):
        """
        Convert an Excel column to a number.
        :param column [str]: Excel column string
        :return [int]: Numeric column string
        """
        func = lambda x, y: x * 26 + y
        ords = (ord(c.upper()) - ord('A') + 1 for c in column)

        return functools.reduce(func, ords)

    def _parse_row(self, tree):
        """
        Parse an XML row and return a list of values.
        :param tree [Element]: ElementTree Element
        :param strings [Element]: Shared string lookup
        :return [list]: Table row
        """
        st, en = self.dimension.split(':')
        st = self._col_to_num(''.join(filter(str.isalpha, st)))
        en = self._col_to_num(''.join(filter(str.isalpha, en)))
        table_range = range(st, en)

        col = nstag(self.NS_MAIN, 'c')
        val = nstag(self.NS_MAIN, 'v')

        row = []
        i = 0
        for cell in tree.iter(col):
            # Insert blank columns if necessary.
            xl_col = ''.join(filter(str.isalpha, cell.attrib.get('r')))
            nm_col = self._col_to_num(xl_col)

            while i < nm_col:
                row.append(None)
                i += 1

            if cell.find(val) is not None:
                value = cell.find(val).text
            else:
                value = None

            if value is None:
                row.append(value)
            elif cell.attrib.get('t'):
                row.append(self._ss_lookup(int(value)))
                """
                FIXME:
                elif cell.attrib.get('s'):
                    num_fmt = cell.attrib.get('s')

                    delta = datetime.timedelta(days=int(value))
                    print(delta)
                    row.append(self.EPOCH + delta)
                """
            else:
                row.append(value)

            i += 1

        return row

    def _set_argparser_options(self):
        """
        Creates an ArgumentParser with the parser's allowed arguments.
        """
        super(XLSXParser, self)._set_argparser_options()

        self._inparser.add_argument('--infile-sheet',
            nargs='?',
            default='Sheet1',
            dest='sheet_name')
        self._inparser.add_argument('--infile-dim',
            dest='dimension')
        self._inparser.add_argument('--infile-no-header',
            action='store_false',
            dest='hasheader')

    def _set_sharedstrings(self, tree):
        """
        Set the shared strings lookup.
        :param tree [Element]: ElementTree element
        """
        self._sharedstrings = list(tree.iter(nstag(self.NS_MAIN, 'si')))

    def _ss_lookup(self, index):
        """
        Return the shared string value at a given index.
        :param index [int]: List index
        :return [str]: Value at index
        """
        return self._sharedstrings[index].find(nstag(self.NS_MAIN, 't')).text

    def read(self, fileobj):
        """
        Open an xlsx archive and read it.
        :param fileobj [File]: Open file object.
        :return [tuple]: header, rows tuple.
        """
        archive = zipfile.ZipFile(fileobj, 'r')
        workbook = ElementTree.fromstring(archive.read(self.WORKBOOK))

        self._set_sharedstrings(ElementTree.fromstring(archive.read(self.STRINGS)))

        tgt = None
        sheets = list(workbook.iter(nstag(self.NS_MAIN, 'sheet')))
        for sheet in sheets:
            if sheet.attrib.get('name') == self.sheet_name:
                tgt = sheet.attrib.get('sheetId')

        if tgt is None:
            raise InvalidSheetNameError(self.sheet_name, 
                options=(x.attrib.get('name') for x in sheets))

        sheet = ElementTree.fromstring(archive.read(self.WORKSHEET.format(tgt)))
        table = sheet.iter(nstag(self.NS_MAIN, 'row'))

        if self.dimension is None:
            self.dimension = sheet.find(nstag(self.NS_MAIN, 'dimension')).attrib.get('ref')

        header = self._parse_row(next(table))
        rows = [self._parse_row(x) for x in table]

        return header, rows

    # XXX Not yet supported
    #def write(self, fileobj):
    #    """
    #    """


class InvalidSheetNameError(Exception):
    MESSAGE = "Sheet '{}' is not in workbook. Please select " \
        "one of the following: {}"

    def __init__(self, sheet, options=None):
        self.sheet = sheet
        self.options = ', '.join(options) if options is not None else ''

    def __str__(self):
        return self.MESSAGE.format(self.sheet, self.options)
