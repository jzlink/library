#!/usr/bin/python
import yaml
import pprint

from database import *

class Queries:
    '''Build queries to DB for website  using yaml metadata'''

    def __init__(self):
        '''load all relevant YAML files'''
        self.OutputTables =  yaml.load(open('OutputTables.yml'))
        self.DBTables = yaml.load(open('DBtables.yml'))


    def show(self, stuff):
        pprint.pprint(stuff)

def test():  
   Q = Queries()
   Q.show(self.DBTables)

if __name__ == '__main__':
    test()
