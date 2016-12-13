# Parsers

Parsers define read and write methods for tabular files.


### Define a Parser

Parsers can be defined externally and hooked into this module by using setuptools.

For example a parser can be defined like so:

```python
# myparser.py
from csvutils.parsers import base


class MyParser(base.Parser):
    
    def write(self, fileobj):
        """
        Prefix each row with a number
        """
        for i, row in enumerate(self.rows):
            fileobj.write(str(i) + ' ' + ' '.join(row) + '\n')

```

You can then register your parser using Entry Points:

```python
# setup.py
from setuptools import setup


setup(
    name='my_module',
    packages=['myparser'],
    entry_points={
        'csvutils.parsers': 'myparser = myparser.myparser:MyParser'
    })
```

Now the parser is available as part of the csvutils library
```bash
csvconvert -f csv -t myparser file.csv
```
