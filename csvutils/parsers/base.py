#
# base.py
#

import argparse
import sys


class Parser(object):
    """
    Base Parser class. Defines the the required methods and attributes.
    """
    READ_MODE = 'r'
    WRITE_MODE = 'w'

    def __init__(self, designation, *args, **kwargs):
        self.header = None
        self.rows = None
        self.designation = designation
        self._set_argparser_options()
        self._parse_args(kwargs.get('parser_options', []))

    def _generic_header(self, columns, prefix='col'):
        """
        Generate a list of generic header columns if the file
        does not have a header.
        :param columns [int]: Number of columns to generate
        :option prefix [str]: Generic column name prefix. Default 'col'
        :return [list]: Generic column list
        """
        return ['{}{}'.format(prefix, x) for x in range(columns)]

    def _parse_args(self, options):
        """
        Parse options with the argument parser.  All parsed options will
        be available as attributes of the parser object.
        :param options [list]: Arguments to parse.
        """
        args = getattr(self, '_' + self.designation).parse_args(options)

        for key, value in vars(args).items():
            setattr(self, key, value)

    def _set_argparser_options(self):
        """
        Creates an ArgumentParser with the parser's allowed arguments.
        """
        self._inparser = argparse.ArgumentParser()
        self._outparser = argparse.ArgumentParser()

        self._inparser.add_argument('infile', nargs='?',
            type=argparse.FileType(self.READ_MODE),
            default=sys.stdin)

        self._outparser.add_argument('-o', '--outfile', nargs='?',
            type=argparse.FileType(self.WRITE_MODE),
            default=sys.stdout)

    def read(self, *args, **kwargs):
        raise NotImplementedError

    def write(self, *args, **kwargs):
        raise NotImplementedError
