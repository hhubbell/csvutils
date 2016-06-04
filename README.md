# CSV Utils

A useful group of utilities for exploring and manipulating csv files.

## Utilities
#### csvavg
`usage: csvavg [-h] [-a] [-d DELIM] [-p PRECISION] [-t] [infile] ...`

Average columns of a csv and print the result to stdout. Optionally,
tabulate and alphabetize output.
```bash
$ csvavg file.csv Margin%
Margin%: .35
```

#### csvdrop
`usage: csvdrop [-h] [-d DELIM] [infile] cols [cols ...]`

Drop columns from a csv and print the result to stdout.  This can be useful
for comparing a file before and after a change is made, if the change includes
adding a new files.  For example, the result of a SQL query:
```bash
$ psql dbname -c "COPY (`cat before.sql`) TO STDOUT WITH CSV HEADER" > before.csv
$ psql dbname -c "COPY (`cat after.sql`) TO STDOUT WITH CSV HEADER" > after.csv
$ diff <(sort before.csv) <(csvdrop after.csv NewColumn1 | sort)
```

#### csvkeep
`usage: csvkeep [-h] [-d DELIM] [infile] cols [cols ...]`

The opposite of `csvdrop`; keep only the columns listed.
```bash
$ csvkeep file.csv name
name
Joe
Larry
Kim
```

#### csvsum
`usage: csvsum [-h] [-a] [-d DELIM] [-p PRECISION] [-t] [infile] ...`

Sum columns of a csv and print the result to stdout.  Optionally,
tabulate and alphabetize output.
```bash
$ csvsum file.csv Subtotal Tax Margin
Subtotal: 1000000
Tax: 40000
Margin: 600000

$ csvsum -t file.csv Subtotal Tax Margin
Subtotal: 1000000
Tax:        40000
Margin:    600000
```

#### csvtab:
`usage: csvtab [-h] [-d DELIM] [-m MAXLENGTH] [-p PADDING] [infile]`

Tabulate a csv file for easier viewing and print result to stdout.
```bash
$ csvtab file.csv
name    salary title
John 100000.00 Boss
Jim   88000.00 Peon
Tim    7600.00 Intern

$ csvtab file.csv -m 6
name salary title
John 100... Boss
Jim  880... Peon
Tim  760... Intern
```
