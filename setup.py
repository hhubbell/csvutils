from setuptools import setup

setup(
    name='csvutils',
    version='0.3.0',
    description='A group of utilities for exploring and manipulating csv files.',
    author='Harry Hubbell',
    url='https://github.com/hhubbell/csvutils',
    packages=['csvutils'],
    scripts=[
        'bin/csvavg',
        'bin/csvdrop',
        'bin/csvkeep',
        'bin/csvsum',
        'bin/csvtab',
        'bin/csvtohtml',
        'bin/csvtojson'])
