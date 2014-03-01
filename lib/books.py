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

    def getTerm(self,term):
       '''Behavior: accepts 'term' and holds it for later use'''
       self.term=term

    def retrieveCoreData(self):
        ''' Behavior: returns core data of all titles sorted by author.
        core data= title, author, notes, when read.
        Has an option to filter results by search term self.term if receieved.'''
        
        sql="""
        select book.book_id, title, author, notes, when_read
        from book, book_author, author, when_read 
        where book.book_id=book_author.book_id and
        author.author_id=book_author.author_id and 
        book.book_id=when_read.book_id
        """
        if self.term:
            kwd= "%" + self.term + "%"
            sql= sql + ' and title like "%s"' % kwd

        output=execute(self.connection, sql)
        
        return output


if __name__ == '__main__':
    # test code:
    books = Books()
    term='dog'
    results = books.getBooks()
    kwdtest=books.getTerm(term)
    bNAtest=books.retrieveCoreData()
    print "Num of books:", len(results)
    print kwdtest
    print bNAtest




