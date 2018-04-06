#
# json.py
#

from __future__ import absolute_import
from ..base import Adapter
import json


class JSONAdapter(Adapter):
    TAB_WIDTH = 4

    def __init__(self, *args, **kwargs):
        """
        :option pretty [bool]: Make JSON human-readable
        """
        super(JSONAdapter, self).__init__(*args, **kwargs)

        self.pretty = kwargs.get('pretty', False)
        self.indent = kwargs.get('indent', self.TAB_WIDTH)

    def _set_argparse_options(self):
        """
        Creates an ArgumentParser with the adapter's allowed arguments.
        """
        super(JSONAdapter, self)._set_argparser_options()

        self._outparser.add_argument('-P', '--outfile-pretty',
            action='store_true',
            dest='pretty',
            help='A flag to indicate the output should be human-readable.')
        # XXX Does not work
        self._outparser.add_argument('-i', '--outfile-indent',
            type=int,
            nargs='?',
            default=self.TAB_WIDTH,
            dest='indent',
            help='The width of an indent. Only valid when the ' \
                'outfile-pretty flag is also used. Default 4 spaces.')

    def write(self, fileobj):
        """
        Dump a json object to an open file handle
        :param fileobj [File]: File object to write to
        """
        indent = self.indent if self.pretty else None
        obj = [{k: v for k, v in zip(self.header, row)} for row in self.rows]

        json.dump(obj, fileobj, indent=indent, sort_keys=self.pretty)
