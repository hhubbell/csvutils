#
# common_table.py
#


class CommonTable(object):
    """
    CommonTable abstraction provides consistent access of tabular objects.
    """

    def __init__(self, header, rows):
        self.header = header
        self.rows = rows

    def __iter__(self):
        if self.header is not None:
            yield self.header

        for row in self.rows:
            yield row
