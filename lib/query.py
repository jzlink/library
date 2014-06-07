#!/usr/bin/env python

from pprint import pprint

from loadyaml import LoadYaml
from database import *

class Query(object):

    def __init__(self):
        dictionary = LoadYaml()
        self.columns = dictionary.loadYaml('columns')
        self.DBTables = dictionary.loadYaml('DBTables')        
        self.OTables = dictionary.loadYaml('OutputTables')
        self.connection = getConnection()

    def getTable(self, table): #, filter=None):
        '''builds dynamic sql to get data for requested table
           return query results'''


        # select
        columns = []
        for rec in self.OTables[table]:
            columns.append(rec['display_name'])

        selects = []
        ftable = []
        x = len(columns)
        i = 0
        while i < x:
            c = columns[i]
            for rec in self.columns[c]:
                selects.append(rec['select'])
                ftable.append(rec['from'])
                i = i + 1

        # from
        ftable  = list(set(ftable))
        joins = []
        y = len(ftable)
        j = 0
        while j < y:
            f = ftable[j]
            for rec in self.DBTables[f]:
                joins.append(rec['join_book'])
                j = j + 1
        joins = sorted(joins)

        # Where
        pass

        # Groupby
        groupbys = []
        groupbys.append('book.title')

        # put it together
        sql = 'select '   
        sql += ','.join(selects)
        sql += ' from '
        sql += ' '.join(joins)
        sql += ' group by '
        sql += ' '.join(groupbys)
        sql = sql.replace('\n', ' ')

        results = execute(self.connection, sql)
        return sql

#debug
DEBUG_SQL = 0

if DEBUG_SQL:
    print 'sql:'
    print sql

def test():  
    test = Query()
    data = test.getTable('main')
    pprint(data)

if __name__ == '__main__':
    test()
