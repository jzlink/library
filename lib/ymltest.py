#!/usr/bin/python

import yaml
import pprint

 #YAML
---
library_columns
"""{
   name: title,
  display_name: Title,
  position: 100,
  record_display: True,
  editable: True,
  edit_type: string,
  select: book.title
}"""
---


for data in yaml.load_all(open('ymltest.py')):
    pprint.pprint(data)
