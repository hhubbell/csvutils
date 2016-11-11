

from __future__ import absolute_import
from .base import Parser
import json


class JSONParser(Parser):
    TAB_WIDTH = 4

    def __init__(self, *args, **kwargs):
        super(JSONParser, self).__init__(*args, **kwargs)

        self.pretty = self.TAB_WIDTH if kwargs.get('pretty') else None

    def write(self, fileobj):
        """
        """
        obj = [{k: v for k, v in zip(self.header, row)} for row in self.rows]

        json.dump(obj, fileobj, indent=self.pretty, sort_keys=True)
