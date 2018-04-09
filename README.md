# Polytab

Manipulate tabular files from the command line

## Utilities
#### polytab map
Apply a function on columns of a table and send the result to a file. By
default this is stdout. Optionally, tabulate and alphabetize output.
```bash
usage: polytab map [-h] [-f [INFORMAT]] [-c [COLS [COLS ...]]] [-a]
                   [-p PRECISION] [-t [OUTFORMAT]] [-T]
                   {mean,sum} ...

positional arguments:
  {mean,sum}            Function to apply across all records of a column

optional arguments:
  -h, --help            show this help message and exit
  -f [INFORMAT], --from [INFORMAT]
                        Input file type. Default CSV.
  -c [COLS [COLS ...]], --cols [COLS [COLS ...]]
                        A list of columns. Each column will have an average
                        generated.
  -a, --alphabetize     A flag to indicate the output should be displayed in
                        alphabetical order. This argument is only valid if the
                        output is transposed. Equivalent to piping to sort
                        without any args.
  -p PRECISION, --precision PRECISION
                        The number of decimal places to show.
  -t [OUTFORMAT], --to [OUTFORMAT]
                        Output file type. Default CSV.
  -T, --transpose       A flag to indicate the output should be transposed so
                        that there are two columns and N rows, where N equals
                        the number of columns indicated to average.
```

Example use:
```bash
$ polytab map avg my_file.csv margin_pct
Margin%: .35
```

#### polytab drop
Drop columns from a table and send the result to a new file. By default this
is stdout.
```bash
usage: polytab drop [-h] [-f [INFORMAT]] [-c [COLS [COLS ...]]] ...

optional arguments:
  -h, --help            show this help message and exit
  -f [INFORMAT], --from [INFORMAT]
                        Input file type. Default CSV.
  -c [COLS [COLS ...]], --cols [COLS [COLS ...]]
                        A list of columns. Each column listed will be dropped.
```

Example use:
```bash
polytab drop my_file.csv -c margin_pct margin_dollar
```

#### polytab keep
The opposite of `polytab drop`; keeps only the columns listed.
```bash
usage: polytab keep [-h] [-f [INFORMAT]] [-c [COLS [COLS ...]]] ...

optional arguments:
  -h, --help            show this help message and exit
  -f [INFORMAT], --from [INFORMAT]
                        Input file type. Default CSV.
  -c [COLS [COLS ...]], --cols [COLS [COLS ...]]
                        A list of columns. Each column listed will be kept.
```

Example use:
```bash
$ polytab keep my_file.csv -c name
```

#### polytab tab
Format a tabular file for printing evenly distributed columns.
```bash
usage: polytab tab [-h] [-f [INFORMAT]]

optional arguments:
  -h, --help            show this help message and exit
  -f [INFORMAT], --from [INFORMAT]
                        Input file type. Default CSV.
```

Example use:
```bash
$ polytab tab file.csv
name    salary title
John 100000.00 Boss
Jim   88000.00 Peon
Tim    7600.00 Intern

$ polytab tab file.csv -m 6
name salary title
John 100... Boss
Jim  880... Peon
Tim  760... Intern
```

#### polytab convert
Transform a tabular file of one type to another. Great for formatting stuff in a pipeline.
```bash
usage: polytab convert [-h] [-f [INFORMAT]] [-t [OUTFORMAT]]

optional arguments:
  -h, --help            show this help message and exit
  -f [INFORMAT], --from [INFORMAT]
                        Input file type. Default CSV.
  -t [OUTFORMAT], --to [OUTFORMAT]
                        Output file type. Default CSV.
```

Example use:
```bash
$ polytab convert -f csv -t html file.csv > table.html

$ mysql < sales.sql \
    | polytab convert -d "\t" -t html \
    | pandoc -s -H company_style.css \
    | bcat  # bcat is awesome
```

## Python Library
`polytab` is also a Python library.  All command line functions can be used in a python script.  For instance:
```python
>>> with open('my_csv.csv', 'r') as f:
...     polytab.fmap(f, sum, columns=['Salary'])
...

[('Salary', 1004567)]
```
