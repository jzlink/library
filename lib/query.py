#!/usr/bin/env python

import yaml

from pprint import pprint

from database import *
from utils import loadYaml

class Query(object):
    '''responsible for building and executing dynamic queries dependant
    on metadata'''

    def __init__(self):
        self.columns = loadYaml('columns')
        self.pages = loadYaml('pages')
        self.tablejoins = loadYaml('tablejoins')
        self.connection = getDictConnection()
        self.conn = getConnection()


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


    def getColumnValues(self, column):
        '''accepts a column
        references metadata
        returns a list of lits where the frist element in the list is the 
        id an the second element is the column value of that id.
        one mini list per table row. suitiable for building options in drop
        down menues or auto complete lists
        '''
        sql= 'select %s from %s'\
            % (self.columns[column][0]['drop_down_select'],
               self.columns[column][0]['foreign_table'])

        results = execute(self.conn, sql)

        return results

def test():  
    test = Query()
    data = test.getSQL('edit', 'book.book_id = 328', None)
#    data = test.getData('edit', 'book.book_id = 1', None)
    print data

if __name__ == '__main__':
    test()
