#
# base.py
#
"""
    Define the abstract Adapter class. This class provides scaffolding for the
    minimum viable adapter object. All adapters must provide either a `read`
    or a `write` method. In practice neither `read` nor `write` need to provide
    any local file I/O; its possible for instance that `write` pushes a stream
    of data to an external URI.

    adapter.read must return an iterable in a matrix like structure. The
    CommonTable class provides this abstraction.

    adapter.write must accept an iterable in matrix form as one of its
    arguments. The CommonTable class provides this abstraction.
"""


import argparse
import sys


def adapter(method, *args, **kwargs):
    """
    Takes a string adapter method name, either `reader` or `writer` and
    returns the appropriate adapter class. This method exists primarily
    to support dynamic arguments passed at the command line. Users that
    want to use a `Reader` or `Writer` adapter should do so directly.
    :param method [str]: Adapter method
    :return [object]: Initialized adapter object
    """
    if method == 'reader':
        adapt = Reader()
    elif method == 'writer':
        adapt = Writer()
    else:
        raise AdapterMethodNotSupportedError(method)

    return adapt


class Reader(object):
    """
    Base Reader class. Defines the required method and attribute scaffolding.
    """
    MODE = 'r'

    def _generic_header(self, columns, prefix='col'):
        """
        Generate a list of generic header columns if the file
        does not have a header.
        :param columns [int]: Number of columns to generate
        :option prefix [str]: Generic column name prefix. Default 'col'
        :return [list]: Generic column list
        """
        return ['{}{}'.format(prefix, x) for x in range(columns)]

    def _init_argparser(self):
        """
        Creates an ArgumentParser with the adapter's allowed arguments.
        """
        self._parser = argparse.ArgumentParser()

        self._parser.add_argument('file', nargs='?',
            type=argparse.FileType(self.MODE),
            default=sys.stdin,
            help='Input file.')

    def parse_args(self, options):
        """
        Initialize argument parse and parse options. All parsed options will
        be available as attributes of the adapter object. The argument parser
        will not be constructed until this method is called.

        :param options [list]: Arguments to parse.
        """
        self._init_argparser()

        args, remainder = self._parser.parse_known_args(options)

        for key, value in vars(args).items():
            setattr(self, key, value)

    def read(self, *args, **kwargs):
        raise NotImplementedError


class Writer(object):
    """
    Base Writer class. Defines the required method and attribute scaffolding.
    """
    MODE = 'w'

    def __init__(self, *args, **kwargs):
        self.data = None

    def _generic_header(self, columns, prefix='col'):
        """
        Generate a list of generic header columns if the file
        does not have a header.
        :param columns [int]: Number of columns to generate
        :option prefix [str]: Generic column name prefix. Default 'col'
        :return [list]: Generic column list
        """
        return ['{}{}'.format(prefix, x) for x in range(columns)]

    def _init_argparser(self):
        """
        Creates an ArgumentParser with the adapter's allowed arguments.
        """
        self._parser = argparse.ArgumentParser()

        self._parser.add_argument('-o', '--outfile', nargs='?',
            type=argparse.FileType(self.MODE),
            default=sys.stdout,
            dest='file',
            help='Output file.')

    def parse_args(self, options):
        """
        Initialize argument parse and parse options. All parsed options will
        be available as attributes of the adapter object. The argument parser
        will not be constructed until this method is called.

        :param options [list]: Arguments to parse.
        """
        self._init_argparser()

        args, remainder = self._parser.parse_known_args(options)

        for key, value in vars(args).items():
            setattr(self, key, value)

    def write(self, *args, **kwargs):
        raise NotImplementedError


class AdapterMethodNotSupportedError(Exception):
    def __init__(self, method=None):
        self.method = method

    def __str__(self):
        method_str = "'{}'".format(self.method) if self.method is not None else ''

        return 'Adapter method {} not supported'.format(method_str)
