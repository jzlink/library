#!/usr/bin/env python
import yaml
from pprint import pprint

import config

class Metadata(object):

    def __init__(self):
        self.conf = config.getInstance()
        self.ordered_cols = []
        self.col_attributes = []
        self.matching_cols = []
        

    def loadYaml(self, name):
        filename = '%s/conf/%s.yml' % (self.conf['basedir'], name)
        dictionary  = yaml.load(open(filename, 'r'))
        return dictionary

    def interrogateMetadata(self, page, attribute):
        '''given a page and column attribute 
        return a dictionary of lists:
        ordered_cols: columns in display order
        col_attributes: a list of lists featuring the col and its attribute
                        value
        matching_cols: a list of columns having a feature'''

        pages = self.loadYaml('pages')
        columns = self.loadYaml('columns')
        ordered_cols = []
        col_attributes = []
        matching_cols = []

        #makes list of columns in display order
        for col in pages[page]:
            ordered_cols.append(col)
        if 'book_id' in ordered_cols:
            ordered_cols.remove('book_id')
        
        for col in ordered_cols:
            x = []
        #adds info to correct list if col has attribute
            for element in columns[col]:
                    if attribute in element:
                        matching_cols.append(col)
                        x.append(col)
                        x.append(element[attribute])                        
                        col_attributes.append(x)

        results = {'ordered_cols': ordered_cols,
                   'col_attributes':col_attributes,
                   'matching_cols': matching_cols}

        return results
   
#test
def test():  
    metadata = Metadata()
   # columns = metadata.loadYaml('columns')
   # pprint(columns)

    test = metadata.interrogateMetadata('main', 'foreign_table')
    print test['matching_cols']

if __name__ == '__main__':
    test()
