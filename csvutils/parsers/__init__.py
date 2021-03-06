#
# Dynamically load parsers from entry points. Ignore modules if
# they have already been imported, or if they raise an exception.
#
# TODO: Determine which exceptions occur.
# TODO: Raise warning on repeat import.
#

import sys
import pkg_resources


for _ep in pkg_resources.iter_entry_points('csvutils.parsers'):
    _mod = __import__(_ep.module_name, fromlist=_ep.attrs)
    setattr(sys.modules[__name__], _ep.name, getattr(_mod, _ep.attrs[0]))

# FIXME Better way to clean these up?
del _ep
del _mod
