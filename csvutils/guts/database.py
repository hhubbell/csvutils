#
# Utilities for creating and managing sqlite databases from csv files
#


from __future__ import print_function
import sqlite3


class SQLiteREPL(object):
    """
    """
    def __init__(self, connection, name=None):
        self.connection = connection
        self.name = name or 'sqlite'

    def start(self):
        """
        Enter REPL and do not exit.
        """
        cursor = self.connection.cursor()

        while True:
            try:
                command = raw_input('{}> '.format(self.name))
                if command == '\q' or command == 'exit':
                    return
            except EOFError:
                print()
                return
            except KeyboardInterrupt:
                print()
                continue

            try:
                cursor.execute(command)
                result = cursor.fetchall()
            except sqlite3.OperationalError as err:
                result = err

            print(result)
