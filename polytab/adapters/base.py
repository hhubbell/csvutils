#
# base.py
#

import argparse
import sys


class Adapter(object):
    """
    Base Adapter class. Defines the the required methods and attributes.
    """
    READ_MODE = 'r'
    WRITE_MODE = 'w'

    def __init__(self, *args, **kwargs):
        self.header = None
        self.rows = None
        self.designation = kwargs.get('designation')
        self._set_argparser_options()

    def _generic_header(self, columns, prefix='col'):
        """
        Generate a list of generic header columns if the file
        does not have a header.
        :param columns [int]: Number of columns to generate
        :option prefix [str]: Generic column name prefix. Default 'col'
        :return [list]: Generic column list
        """
        return ['{}{}'.format(prefix, x) for x in range(columns)]

    def _set_argparser_options(self):
        """
        Creates an ArgumentParser with the adapter's allowed arguments.
        """
        self._inparser = argparse.ArgumentParser()
        self._outparser = argparse.ArgumentParser()

        self._inparser.add_argument('file', nargs='?',
            type=argparse.FileType(self.READ_MODE),
            default=sys.stdin,
            help='Input file.')

        self._outparser.add_argument('-o', '--outfile', nargs='?',
            type=argparse.FileType(self.WRITE_MODE),
            default=sys.stdout,
            dest='file',
            help='Output file.')

    def parse_args(self, options):
        """
        Parse options with the argument parser.  All parsed options will
        be available as attributes of the adapter object.
        :param options [list]: Arguments to parse.
        """
        try:
            parser = '_' + self.designation
            args, remainder = getattr(self, parser).parse_known_args(options)

            for key, value in vars(args).items():
                setattr(self, key, value)

        except AttributeError:
            raise NoAdapterDesignationError

    def read(self, *args, **kwargs):
        raise NotImplementedError

    def write(self, *args, **kwargs):
        raise NotImplementedError


class NoAdapterDesignationError(Exception):

    def __str__(self):
        return 'Adapter has no designation defined.'
