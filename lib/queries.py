#!/usr/bin/python
import yaml
import pprint

from database import *

class Queries(object):
    '''Build queries to DB for website  using yaml metadata'''

    def __init__(self):
        '''load all relevant YAML files'''
        self.OutputTables =  yaml.load(open('OutputTables.yml'))
        self.DBTables = yaml.load(open('DBtables.yml'))


    def getTables(self):
        Otables = []
        for k, v in self.OutputTables.items():
           Otables.append(k)
        print Otables
       
        subdic = []
        for d in self.OutputTables['Main']:
           for k, v in d.items():
               print k, v


    def show(self, stuff):
        pprint.pprint(stuff)

def test():  
   Q = Queries()
   stuff = Q.OutputTables
  # Q.show(stuff)
   Q.getTables()
if __name__ == '__main__':
    test()
