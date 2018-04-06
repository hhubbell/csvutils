#
# xlsx_basic.py
#

from __future__ import absolute_import
from ..base import Adapter
import datetime
import functools
import zipfile
import xml.etree.ElementTree as ElementTree


def nstag(ns, tag):
    return '{{{}}}{}'.format(ns, tag)


class XLSXAdapter(Adapter):
    READ_MODE = 'rb'
    WRITE_MODE = 'wb'

    NS_MAIN = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'

    STRINGS = 'xl/sharedStrings.xml'
    XFSTYLE = 'xl/styles.xml'
    WORKBOOK = 'xl/workbook.xml'
    WORKSHEET = 'xl/worksheets/sheet{}.xml'

    EPOCH = datetime.date(1900, 1, 1)

    def __init__(self, *args, **kwargs):
        """
        :option sheet_name [str]: Target sheet
        :option dimension [str]: Excel range notation (A1:B2)
        :option hasheader [bool]: Use first row in table as header
        """
        super(XLSXAdapter, self).__init__(*args, **kwargs)

        self.sheet_name = kwargs.get('sheet_name')
        self.sheet_id = kwargs.get('sheet_id', 1)
        self.dimension = kwargs.get('dimension')
        self.hasheader = kwargs.get('hasheader', True)
        self.start_row = kwargs.get('start_row')
        self.end_row = kwargs.get('end_row')

    def _col_to_num(self, column):
        """
        Convert an Excel column to a number.
        :param column [str]: Excel column string
        :return [int]: Numeric column string
        """
        func = lambda x, y: x * 26 + y
        ords = (ord(c.upper()) - ord('A') + 1 for c in column)

        return functools.reduce(func, ords)

    def _get_display_type(self, cell):
        """
        Return a cell's contents as it would appear on a worksheet.
        :param cell [Element]: Element Tree Element XLSX Cell
        :return [mixed]: String, Decimal, integer, None, etc...
        """
        value = cell.find(nstag(self.NS_MAIN, 'v'))
        content = value.text if value is not None else None

        if content is None:
            display = content
        elif cell.attrib.get('t'):
            display = self._ss_lookup(int(content))
        elif cell.attrib.get('s'):
            num_fmt = int(self._xf_lookup(int(cell.attrib.get('s'))))
            # MVP: Dates (14)
            if num_fmt == 14:
                dv = datetime.timedelta(days=int(content))
                display = (self.EPOCH + dv).strftime('%m/%d/%Y')
            else:
                display = content
        else:
            display = content

        return display

    def _get_sheet(self, archive):
        """
        Find and open the desired worksheet. Prefer sheet_id over sheet_name.
        :param archive [ElementTree]: Open workbook archive
        :return [ElementTree]: Sheet element tree
        """
        workbook = ElementTree.fromstring(archive.read(self.WORKBOOK))
        sheets = list(workbook.iter(nstag(self.NS_MAIN, 'sheet')))

        if self.sheet_id is not None and self.sheet_name is None:
            if 0 < self.sheet_id <= len(sheets):
                sheet = self.sheet_id
            else:
                raise InvalidSheetError(self.sheet_id, 'index',
                    options=(str(x) for x in range(1, len(sheets) + 1)))
        else:
            try:
                names = [x.attrib.get('name') for x in sheets]
                sheet = next(i for i, x in enumerate(names, 1) if x == self.sheet_name)
            except StopIteration:
                raise InvalidSheetError(self.sheet_name, 'name',
                    options=(x.attrib.get('name') for x in sheets))

        return ElementTree.fromstring(archive.read(self.WORKSHEET.format(sheet)))

    def _in_range(self, row):
        """
        Check to make sure a given row is inside the specified range
        of rows. Return boolean result.
        :param row [Element]: Element Tree Element to check.  Must have
            an `r` attribute - the element must be a row.
        :return [bool]: True if the row is within the range.
        """
        index = int(row.attrib['r']) - 1

        if self.start_row is None and self.end_row is None:
            result = True

        elif self.start_row is not None and self.end_row is not None \
          and self.start_row <= index <= self.end_row:
            result = True

        elif self.start_row is not None and self.end_row is None \
          and index >= self.start_row:
            result = True

        elif self.start_row is None and self.end_row is not None \
          and index <= self.end_row:
            result = True

        else:
            result = False

        return result

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
            nm_col = self._col_to_num(xl_col) - 1

            while i < nm_col:
                row.append(None)
                i += 1

            row.append(self._get_display_type(cell))
            i += 1

        return row

    def _set_argparser_options(self):
        """
        Creates an ArgumentParser with the adapter's allowed arguments.
        """
        super(XLSXAdapter, self)._set_argparser_options()

        self._inparser.add_argument('--infile-sheet-name',
            nargs='?',
            dest='sheet_name')
        self._inparser.add_argument('--infile-sheet-index',
            type=int,
            default=1,
            dest='sheet_id')
        self._inparser.add_argument('--infile-dim',
            dest='dimension')
        self._inparser.add_argument('--infile-no-header',
            action='store_false',
            dest='hasheader')
        self._inparser.add_argument('--infile-start-row',
            type=int,
            dest='start_row')
        self._inparser.add_argument('--infile-end-row',
            type=int,
            dest='end_row')

    def _set_sharedstrings(self, tree):
        """
        Set the shared strings lookup.
        :param tree [Element]: ElementTree element
        """
        self._sharedstrings = list(tree.iter(nstag(self.NS_MAIN, 'si')))

    def _set_xfstyles(self, tree):
        """
        Set the xfstyle lookup.
        :param tree [Element]: ElemetTree element
        """
        xftree = tree.find(nstag(self.NS_MAIN, 'cellXfs'))
        self._xfstyles = list(xftree.iter(nstag(self.NS_MAIN, 'xf')))

    def _ss_lookup(self, index):
        """
        Return the shared string value at a given index.
        :param index [int]: List index
        :return [str]: Value at index
        """
        return self._sharedstrings[index].find(nstag(self.NS_MAIN, 't')).text

    def _xf_lookup(self, index):
        """
        Return the style value at a given index.
        :param index [int]: List index
        :return [int]: Value at index
        """
        return self._xfstyles[index].attrib['numFmtId']

    def read(self, fileobj):
        """
        Open an xlsx archive and read it.
        :param fileobj [File]: Open file object.
        :return [tuple]: header, rows tuple.
        """
        archive = zipfile.ZipFile(fileobj, 'r')

        self._set_sharedstrings(ElementTree.fromstring(archive.read(self.STRINGS)))
        self._set_xfstyles(ElementTree.fromstring(archive.read(self.XFSTYLE)))

        sheet = self._get_sheet(archive)
        table = sheet.iter(nstag(self.NS_MAIN, 'row'))

        if self.dimension is None:
            self.dimension = sheet.find(nstag(self.NS_MAIN, 'dimension')).attrib.get('ref')

        rows = [self._parse_row(x) for x in table if self._in_range(x)]
        header = rows.pop(0)

        return header, rows

    # XXX Not yet supported
    #def write(self, fileobj):
    #    """
    #    """


class InvalidSheetError(Exception):
    MESSAGE = "Sheet {} '{}' is not in workbook. Please select " \
        "one of the following: {}"

    def __init__(self, sheet, identifier, options=None):
        self.sheet = sheet
        self.identifier = identifier
        self.options = ', '.join(options) if options is not None else ''

    def __str__(self):
        return self.MESSAGE.format(self.identifier, self.sheet, self.options)
