from setuptools import setup
import os
import re

def get_version():
    with open(os.path.join('polytab', '__init__.py'), 'r') as f:
        return re.search('^__version__ = \'(.*)\'$', f.read(), re.M).group(1)

setup(
    name='polytab',
    version=get_version(),
    description='A group of utilities for exploring and manipulating tabular files.',
    author='Harry Hubbell',
    url='https://github.com/hhubbell/polytab',
    packages=['polytab', 'polytab.parsers', 'polytab.parsers.builtins'],
    entry_points={
        'console_scripts': [
            'polytab=polytab.__main__:main',
            # XXX: DEPRECATED - Leave for now just for testing
            'csvavg=polytab.cli:csvavg',
            'csvconvert=polytab.cli:csvconvert',
            'csvdrop=polytab.cli:csvdrop',
            'csvkeep=polytab.cli:csvkeep',
            'csvsum=polytab.cli:csvsum',
            'csvtab=polytab.cli:csvtab'],
        'polytab.parsers': [
            'csv=polytab.parsers.builtins.csv:CSVParser',
            'html=polytab.parsers.builtins.html:HTMLParser',
            'json=polytab.parsers.builtins.json:JSONParser',
            'table=polytab.parsers.builtins.table:TableParser',
            'xlsx_basic=polytab.parsers.builtins.xlsx_basic:XLSXParser']})
