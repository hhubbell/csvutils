from setuptools import setup
import os
import re

def get_version():
    with open(os.path.join('csvutils', '__init__.py'), 'r') as f:
        return re.search('^__version__ = \'(.*)\'$', f.read(), re.M).group(1)

setup(
    name='csvutils',
    version=get_version(),
    description='A group of utilities for exploring and manipulating csv files.',
    author='Harry Hubbell',
    url='https://github.com/hhubbell/csvutils',
    packages=['csvutils', 'csvutils.parsers'],
    entry_points={
        'console_scripts': [
            'csvavg=csvutils.cli:csvavg',
            'csvconvert=csvutils.cli:csvconvert',
            'csvdrop=csvutils.cli:csvdrop',
            'csvkeep=csvutils.cli:csvkeep',
            'csvsum=csvutils.cli:csvsum',
            'csvtab=csvutils.cli:csvtab']})
