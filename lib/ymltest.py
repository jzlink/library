#!/usr/bin/python

import yaml
import pprint

 #YAML
"""library_columns:
 -name: title
  display_name: Title
  position: 100
  record_display: True
  editable: True
  edit_type: string
  select: book.title
"""
y="""
people:
   - name: david
     color: green

   -  name: jules
      color: blue
"""

y="""
   - name: david
     color: green

   - name: jules
     color: blue
"""

#for data in yaml.load(y):
    #pprint.pprint(data)

#people= yaml.load(y)
#pprint.pprint(people)
#for person in people:
#    print person['name']

people= yaml.load(open('people.yml'))
pprint.pprint(people)
