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
    packages=['polytab', 'polytab.adapters', 'polytab.adapters.builtins'],
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
        'polytab.adapters': [
            'csv=polytab.adapters.builtins.csv:CSVAdapter',
            'html=polytab.adapters.builtins.html:HTMLAdapter',
            'json=polytab.adapters.builtins.json:JSONAdapter',
            'table=polytab.adapters.builtins.table:TableAdapter',
            'xlsx_basic=polytab.adapters.builtins.xlsx_basic:XLSXAdapter']})
