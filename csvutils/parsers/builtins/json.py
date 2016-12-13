

from __future__ import absolute_import
from ..base import Parser
import json


class JSONParser(Parser):
    TAB_WIDTH = 4

    def __init__(self, *args, **kwargs):
        """
        :option pretty [bool]: Make JSON human-readable
        """
        super(JSONParser, self).__init__(*args, **kwargs)

        self.pretty = kwargs.get('pretty', False)
        self.indent = self.TAB_WIDTH if self.pretty else None

    def write(self, fileobj):
        """
        Dump a json object to an open file handle
        :param fileobj [File]: File object to write to
        """
        obj = [{k: v for k, v in zip(self.header, row)} for row in self.rows]

        json.dump(obj, fileobj, indent=self.indent, sort_keys=self.pretty)
