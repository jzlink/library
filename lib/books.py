#!/usr/bin/python
from database import *

class Books:
    '''Preside over Book records in the database'''

    def __init__(self):
        self.connection = getConnection()

    def getBooks(self):
        results = execute(self.connection, 
                          'select book_id, title from book')
        return results

    def retrieveCoreData(self, filter=None, order_by=None):
        ''' Behavior: returns core data of all titles sorted by author.
        core data= title, author, notes, when_read.
        Has an option to filter results by search filter if receieved.'''

        sql="""
   select
      book.book_id, 
      title, 
      group_concat(distinct concat(last_name, ', ', first_name) order by last_name separator ' & ') as author,
      notes, 
      group_concat(distinct when_read separator ' & ') as date
   from 
      book
      left join book_author on book.book_id= book_author.book_id 
      left join author on book_author.author_id= author.author_id
      left join when_read on book.book_id = when_read.book_id
  group by title   
        """
        if filter:
            kwd= "%" + filter + "%"
            sql= sql + ' where title like "%s"' % kwd

        if order_by:
            sql= sql + ' order by %s' % order_by


        output=execute(self.connection, sql)
        
        return output


if __name__ == '__main__':
    # test code:
    order_by = 'title'
    results = Books().retrieveCoreData(filter, order_by)
    print "Filter: %s" % filter
    print "Num of books:", len(results)
    print results
    if not filter:
        print "No"




