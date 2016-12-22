#
# xlsx parser
#

from __future__ import absolute_import
from ..base import Parser
from ...helpers import letters
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

    def _parse_row(self, tree):
        """
        Parse an XML row and return a list of values.
        :param tree [Element]: ElementTree Element
        :param strings [Element]: Shared string lookup
        :return [list]: Table row
        """
        st, en = self.dimension.split(':')
        st = ''.join(filter(str.isalpha, st))
        en = ''.join(filter(str.isalpha, en))
        xl_cols = letters(st, en)

        col = nstag(self.NS_MAIN, 'c')
        val = nstag(self.NS_MAIN, 'v')

        row = []
        i = 0
        for cell in tree.iter(col):
            # Insert blank columns if necessary.
            xl_col =  ''.join(filter(str.isalpha, cell.attrib.get('r')))
            while xl_col != xl_cols[i]:
                row.append(None)
                i += 1

            value = cell.find(val).text

            if cell.attrib.get('t'):
                row.append(self._ss_lookup(int(value)))
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
        for sheet in workbook.iter(nstag(self.NS_MAIN, 'sheet')):
            if sheet.attrib.get('name') == self.sheet_name:
                tgt = sheet.attrib.get('sheetId')

        if tgt is None:
            raise Exception # FIXME csvutils exception

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
