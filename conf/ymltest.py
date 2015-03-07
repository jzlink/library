#!/usr/bin/python

import yaml
from pprint import pprint

pages= yaml.load(open('conf/pages.yml'))
columns = yaml.load(open('conf/columns.yml'))

#pprint(pages['main'])
#print pages['main']

for col in columns:
    print col +': '+  columns[col][0]['type']

