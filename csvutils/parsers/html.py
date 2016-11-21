

from __future__ import absolute_import
from .base import Parser


class HTMLParser(Parser):
    TEMPLATE = '<table>\n{}{}\n</table>\n'
    TAB_WIDTH = 4

    def __init__(self, *args, **kwargs):
        super(HTMLParser, self).__init__(*args, **kwargs)

        self.pretty = kwargs.get('pretty', False)

    def htmlrow(self, row, header=False, tabs=False):
        """
        Format one row of data
        :param row:         Row to format
        :option header:     Header row flag
        :option tabs:       Make html human readable by using \n and \t. Tabs
                            will be TAB_WIDTH
        :return str:        Table row
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

    def write(self, fileobj):
        """
        """
        h = self.htmlrow(self.header, header=True, tabs=self.pretty) + '\n' if self.header else ''
        r = (self.htmlrow(x, tabs=self.pretty) for x in self.rows)

        fileobj.write(self.TEMPLATE.format(h, '\n'.join(r)))
