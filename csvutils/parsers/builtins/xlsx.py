#
# xlsx parser
#

from __future__ import absolute_import
from ..base import Parser
import zipfile


class XLSXParser(Parser):
    
    def __init__(self, *args, **kwargs):
        """
        """
        super(XLSXParser, self).__init__(*args, **kwargs)

    def read(self, fileobj):
        """
        Open an xlsx archive and read it.
        :param fileobj [File]: Open file object.
        :return [tuple]: header, rows tuple.
        """
    
    def write(self, fileobj):
        """
        """
