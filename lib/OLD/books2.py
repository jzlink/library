#!/usr/bin/env python

from columns import Columns
from database import *

DEBUG_SQL = 1

class Books(object):

    def __init__(self):
        self.columns = Columns().columns
        self.connection = getConnection()

    def getData(self): #, filter=None):
        '''Build Dyamic SQL
           return query results'''

        # select
        selects = []
        for rec in self.columns['record']:
            selects.append(rec['select'])

        # from
        froms = []
        froms.append('book b')
        froms.append('left join book_author ba on ba.book_id=b.book_id')
        froms.append('left join author a on a.author_id = ba.author_id')
        froms.append('left join when_read wr on b.book_id = wr.book_id')
        froms.append('left join series s on b.series_id = s.series_id')
        froms.append('left join owner_status os on '
                     'b.owner_status_id = os.owner_status_id')
        froms.append('left join read_status rs on '
                     'b.read_status_id = rs.read_status_id')
        froms.append('left join type t on b.type_id = t.type_id')

        # Where
        pass

        # Groupby
        groupbys = []
        groupbys.append('b.title')

        # put it together
        sql = 'select\n   '

        sql += ',\n   '.join(selects)
        sql += '\nfrom\n   '
        sql += '\n   '.join(froms)
        sql += '\ngroup by\n   '
        sql += '\n   '.join(groupbys)
        if DEBUG_SQL:
            print 'sql:'
            print sql

        results = execute(self.connection, sql)
        return results

books = Books()
#print books.columns

i = 0
for book in books.getData():
    print i, book
    i += 1
