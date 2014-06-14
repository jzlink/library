#!/usr/bin/env python

from pprint import pprint

from loadyaml import LoadYaml
from database import *

class Query(object):

    def __init__(self):
        loadyaml = LoadYaml()
        self.columns = loadyaml.loadYaml('columns')
        self.tablejoins = loadyaml.loadYaml('tablejoins')        
        self.pages = loadyaml.loadYaml('pages')
        self.connection = getConnection()

    def getData (self, page, filter = None, sort = None):
        ''' accepts request for page, calls SQL builder, executes SQL
        returns query results'''

        sql = self.getSQL(page, filter)
        results = execute(self.connection, sql)
        return results

    def getSQL(self, page, filter = None, sort = None):
        '''builds dynamic sql for requested table
           return sql string'''

        # select
        columns = []
        for rec in self.pages[page]:
            columns.append(rec['column'])

        selects = []
        froms = []
        for c in columns:
            for rec in self.columns[c]:
                selects.append(rec['select'])
                froms.append(rec['from'])

        # from
        froms  = list(set(froms))
        joins = []

        for f in froms:
            for rec in self.tablejoins[f]:
                joins.append(rec['join_book'])
        
        # HACK. to make sure book goes to top of from stmt.
        joins = sorted(joins)

        # Where
        where = ''
        if filter:
            where = 'where ' + filter
            
        # Groupby
        groupbys = []
        groupbys.append('book.title')

        
        #Order by
        order = ''
        if sort:
            order = 'order by ' + sort 
        
        # put it together
        sql = 'select '   
        sql += ','.join(selects)
        sql += ' from '
        sql += ' '.join(joins)
        sql += ' ' + where
        sql += ' group by '
        sql += ' '.join(groupbys)
        sql += ' ' + order

        return sql


def test():  
    test = Query()
    data = test.getSQL('main', None, 'title')
#    data = test.getData('main', 'book.book_id > 475, 'title')
    print data

if __name__ == '__main__':
    test()
