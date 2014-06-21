#!/usr/bin/python

import yaml
import pprint

pages= yaml.load(open('conf/pages.yml'))
columns = yaml.load(open('conf/columns.yml'))
#pprint.pprint(stuff)

 # get list of columns assigned to each page
cols = []
for rec in pages['main']:
    cols.append(rec)

# retrieve select statement and from table for each column
selects = []
from_raw = []
for c in cols:
    for rec in columns[c]:
        selects.append(rec['select'])
        from_raw.append(rec['from'])

print selects
print from_raw

