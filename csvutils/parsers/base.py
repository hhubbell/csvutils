

class Parser(object):
    """
    Base Parser class. Define the the required methods.
    """
    def __init__(self, *args, **kwargs):
        self.header = None
        self.rows = None

        self.pretty = None

    def _generic_header(self, columns, prefix='col'):
        """
        Generate a list of generic header columns if the file
        does not have a header.
        :param columns:     Number of columns to generate
        :option prefix:     Generic column name prefix
        :return list:       Generic column list
        """
        return ['{}{}'.format(prefix, x) for x in range(columns)]

    def read(self, *args, **kwargs):
        raise NotImplementedError

    def write(self, *args, **kwargs):
        raise NotImplementedError
