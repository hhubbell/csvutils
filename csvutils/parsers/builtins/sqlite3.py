#
#
#

from __future__ import absolute_import
from ..base import Parser
from ...guts.helpers import quote
from os import path
import sqlite3


class SQLite3Parser(Parser):

    def __init__(self, *args, **kwargs):
        """
        """
        super(SQLite3Parser, self).__init__(*args, **kwargs)
        self.table_name = kwargs.get('table_name')

    def _create_schema(self, table, header):
        return 'CREATE TABLE {} ({})'.format(table, ', '.join(header))

    def _create_insert(self, table, header, rows):
        return  'INSERT INTO {} ({}) VALUES {}'.format(table,
            ', '.join(header),
            ', '.join('({})'.format(', '.join(quote(y) for y in x)) for x in rows))

    def read(self, fileobj):
        """
        Open a SQLite3 database and read it.
        :param fileobj [File]: Open file object
        """
        conn = sqlite3.connect(fileobj.name)

    def write(self, fileobj):
        """

        """
        conn = sqlite3.connect(fileobj.name)
        cur = conn.cursor()

        if self.table_name is None:
            self.table_name = path.splitext(path.basename(fileobj.name))[0]

        cur.execute(self._create_schema(self.table_name, self.header))
        cur.execute(self._create_insert(self.table_name, self.header, self.rows))

        conn.commit()
        conn.close()
