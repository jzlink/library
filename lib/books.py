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

    def retrieveCoreData(self, filter=None):
        ''' Behavior: returns core data of all titles sorted by author.
        core data= title, author, notes, when read.
        Has an option to filter results by search filter if receieved.'''

        sql="""
        select book.book_id, title, author, notes, when_read
        from book, book_author, author, when_read 
        where book.book_id=book_author.book_id and
        author.author_id=book_author.author_id and 
        book.book_id=when_read.book_id
        """
        if filter:
            kwd= "%" + filter + "%"
            sql= sql + ' and title like "%s"' % kwd

        output=execute(self.connection, sql)
        
        return output


if __name__ == '__main__':
    # test code:
    filter = 'dog'
    results = Books().retrieveCoreData(filter)
    print "Filter: %s" % filter
    print "Num of books:", len(results)




