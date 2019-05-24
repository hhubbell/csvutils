#
# json.py
#

from __future__ import absolute_import
from ..base import Writer, AdapterMethodNotSupportedError
import json


def adapter(method, *args, **kwargs):
    """
    Takes a string adapter method name, either `reader` or `writer` and
    returns the appropriate adapter class. This method exists primarily
    to support dynamic arguments passed at the command line. Users that
    want to use a `JSONReader` or `JSONWriter` adapter should do so directly.
    :param method [str]: Adapter method
    :return [object]: Initialized adapter object
    """
    if method == 'reader':
        # Not currently supported
        raise AdapterMethodNotSupportedError(method)
    elif method == 'writer':
        adapt = JSONWriter()
    else:
        raise AdapterMethodNotSupportedError(method)

    return adapt


class JSONWriter(Writer):
    TAB_WIDTH = 4

    def __init__(self, *args, **kwargs):
        """
        :option pretty [bool]: Make JSON human-readable
        :option indent [int]: Override indentation width
        """
        super(JSONWriter, self).__init__(*args, **kwargs)

        self.pretty = kwargs.get('pretty', False)
        self.indent = kwargs.get('indent', self.TAB_WIDTH)

    def _set_argparse_options(self):
        """
        Creates an ArgumentParser with the adapter's allowed arguments.
        """
        super(JSONWriter, self)._set_argparser_options()

        self._parser.add_argument('-P', '--outfile-pretty',
            action='store_true',
            dest='pretty',
            help='A flag to indicate the output should be human-readable.')
        # XXX Does not work
        self._parser.add_argument('-i', '--outfile-indent',
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
        obj = [{k: v for k, v in zip(self.data.header, row)} for row in self.data.rows]

        json.dump(obj, fileobj, indent=indent, sort_keys=self.pretty)
