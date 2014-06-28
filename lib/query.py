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
        self.connection = getDictConnection()

    def getData (self, page, where = None, sort = None):
        ''' accepts request for page, calls SQL builder, executes SQL
        returns query results'''

        sql = self.getSQL(page, where, sort)
        results = execute(self.connection, sql)
        return results

    def getSQL(self, page, filter = None, sort = None):
        '''builds dynamic sql for requested table
           return sql string'''

        # get list of columns assigned to each page
        columns = []
        for rec in self.pages[page]:
            columns.append(rec)

        # retrieve select statement and from table for each column
        selects = []
        from_raw = []
        for c in columns:
            for rec in self.columns[c]:
               select = rec['select']
              # display = rec['display']
               select_stmt = select + " as " + c
               selects.append(select_stmt)
               from_raw.append(rec['from'])

        # get join statments and order them properly for use in from clause
        from_raw  = list(set(from_raw))
        joins = []
        for f in from_raw:
            for rec in self.tablejoins[f]:
                joins.append(rec['join_book'])
        
        froms = []
        for j in joins:
            if "join" not in j:
                froms.append(j)
                joins.remove(j)               
        for j in joins:
            froms.append(j)

        # bulid where clause if filter provided
        where = ''
        if filter:
            where = 'where ' + filter
            
        # Group by
        groupbys = []
        groupbys.append('book.title')

        
        #build order clause if sort provided
        order = ''
        if sort:
            order = 'order by ' + sort 
        
        # put elements together to make functioning sql query
        sql = 'select '   
        sql += ', '.join(selects)
        sql += ' from '
        sql += ' '.join(froms)
        sql += ' ' + where
        sql += ' group by '
        sql += ' '.join(groupbys)
        sql += ' ' + order

        return sql


def test():  
    test = Query()
#    data = test.getSQL('record', 'book.book_id > 475', 'title')
    data = test.getData('main', 'book.book_id = 475', None)
    print data

if __name__ == '__main__':
    test()
