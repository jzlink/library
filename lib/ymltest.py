#!/usr/bin/python

import yaml
import pprint

#for data in yaml.load(y):
    #pprint.pprint(data)

#people= yaml.load(y)
#pprint.pprint(people)
#for person in people:
#    print person['name']

stuff= yaml.load(open('OutputTables.yml'))
pprint.pprint(stuff)
