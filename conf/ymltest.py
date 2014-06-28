#!/usr/bin/python

import yaml
from pprint import pprint

pages= yaml.load(open('conf/pages.yml'))
columns = yaml.load(open('conf/columns.yml'))

#pprint(pages['main'])
#print pages['main']

col_order= []
for item in pages['main']:
    col_order.append(item)

print col_order
