from setuptools import setup

setup(
    name='csvutils',
    version='0.5.0',
    description='A group of utilities for exploring and manipulating csv files.',
    author='Harry Hubbell',
    url='https://github.com/hhubbell/csvutils',
    packages=['csvutils'],
    entry_points={
        'console_scripts': [
            'csvavg=csvutils.cli:csvavg',
            'csvdrop=csvutils.cli:csvdrop',
            'csvkeep=csvutils.cli:csvkeep',
            'csvsum=csvutils.cli:csvsum',
            'csvtab=csvutils.cli:csvtab',
            'csvtohtml=csvutils.cli:csvtohtml',
            'csvtojson=csvutils.cli:csvtojson']})
