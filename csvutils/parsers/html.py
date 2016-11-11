

from __future__ import absolute_import
from .base import Parser


class html(Parser):
    TEMPLATE = '<table>\n{}{}\n</table>\n'
    TAB_WIDTH = 4

    def __init__(self, *args, **kwargs):
        super(self, html).__init__(*args, **kwargs)

        self.pretty = self.TAB_WIDTH if kwargs.get('pretty') else None

    def htmlrow(row, header=False, tabs=False):
        """
        Format one row of data
        :param row:         Row to format
        :option header:     Header row flag
        :option tabs:       Make html human readable by using \n and \t. Tabs
                            will be TAB_WIDTH
        :return str:        Table row
        """
        tabf = ' ' * self.TAB_WIDTH if tabs is not False else ''
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
        h = self.htmlrow(header, header=True, tabs=pretty) + '\n' if header else ''
        r = (self.htmlrow(x, tabs=self.pretty) for x in rows)

        fileobj.write(self.TEMPLATE.format(h, '\n'.join(r)))
