# Adapters

Adapters define read and write methods for tabular files.


### Define an Adapter

Adapters can be defined externally and hooked into this module by using setuptools.

For example an adapter can be defined like so:

```python
# myadapter.py
from polytab.adapters import base


class MyAdapter(base.Adapter):
    
    def write(self, fileobj):
        """
        Prefix each row with a number
        """
        for i, row in enumerate(self.rows):
            fileobj.write(str(i) + ' ' + ' '.join(row) + '\n')

```

You can then register your adapter using Entry Points:

```python
# setup.py
from setuptools import setup


setup(
    name='my_module',
    packages=['myadapter'],
    entry_points={
        'polytab.adapters': 'myadapter = myadapter.myadapter:MyAdapter'
    })
```

Now the adapter is available as part of the polytab library
```bash
csvconvert -f csv -t myadapter file.csv
```
