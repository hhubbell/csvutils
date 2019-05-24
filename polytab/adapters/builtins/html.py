#
# html.py
#

from __future__ import absolute_import
from ..base import Writer, AdapterMethodNotSupportedError


def adapter(method, *args, **kwargs):
    """
    Takes a string adapter method name, either `reader` or `writer` and
    returns the appropriate adapter class. This method exists primarily
    to support dynamic arguments passed at the command line. Users that
    want to use a `HTMLReader` or `HTMLWriter` adapter should do so directly.
    :param method [str]: Adapter method
    :return [object]: Initialized adapter object
    """
    if method == 'reader':
        # Not currently supported
        raise AdapterMethodNotSupportedError(method)
    elif method == 'writer':
        adapt = HTMLWriter()
    else:
        raise AdapterMethodNotSupportedError(method)

    return adapt


class HTMLWriter(Writer):
    TEMPLATE = '<table>\n{}{}\n</table>\n'
    TAB_WIDTH = 4

    def __init__(self, *args, **kwargs):
        """
        :option pretty [bool]: Make HTML human-readable
        """
        super(HTMLWriter, self).__init__(*args, **kwargs)

        self.pretty = kwargs.get('pretty', getattr(self, 'pretty', False))

    def _htmlrow(self, row, header=False, tabs=False):
        """
        Format one row of data
        :param row [iter]: Row to format
        :option header [bool]: Header row flag
        :option tabs [bool]: Make html human-readable by using \n and \t.
            Tabs will be TAB_WIDTH
        :return [str]: Table row
        """
        tabf = ' ' * self.TAB_WIDTH if tabs is True else ''
        newl = '\n' if tabs is True else ''
        joiner = '{}{}'.format(newl, tabf * 2)

        col = '<td>{}</td>' if header is False else '<th>{}</th>'
        return '{t}<tr>{j}{col}{n}{t}</tr>'.format(
            col=joiner.join(col.format(x) for x in row),
            j=joiner,
            n=newl,
            t=tabf)

    def _set_argparser_options(self):
        """
        Creates an ArgumentParser with the adapters's allowed arguments.
        """
        super(HTMLWriter, self)._set_argparser_options()

        self._parser.add_argument('-P', '--outfile-pretty',
            action='store_true',
            dest='pretty',
            help='A flag to indicate the output should be human-readable.')

    def write(self, fileobj):
        """
        Dump a html table to an open file handle
        :param fileobj [File]: File object to write to
        """
        h = self._htmlrow(self.data.header, header=True, tabs=self.pretty) + '\n' if self.data.header else ''
        r = (self._htmlrow(x, tabs=self.pretty) for x in self.data.rows)

        fileobj.write(self.TEMPLATE.format(h, '\n'.join(r)))
