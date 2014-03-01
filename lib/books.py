#!/usr/bin/python
from database import *

class Books:
    '''Preside over Book records in the database'''

    def __init__(self):
        self.connection = getConnection()
       # if term:
        #    self.term=term
         #   kwd= "%" + self.term + "%"

    def getBooks(self):
        results = execute(self.connection, 
                          'select book_id, title from book')
        return results

    def getTerm(self,term):
       '''accepts term and returns term with % to either end of it for use in query'''
       self.term=term
       self.term= "%" + self.term + "%"

    

    def booksNotesAuthors (self):
        ''' Behavior: returns a list of all books, authors, and notes
        sorted by author'''
        
        sql="""
        select book.book_id, title, author, notes, when_read
        from book, book_author, author, when_read 
        where book.book_id=book_author.book_id and
        author.author_id=book_author.author_id and 
        book.book_id=when_read.book_id
        """
        if self.term:
           # a.getTerm(term)
           # search=" and title like '%s'" % self.term
            sql= """
            select book.book_id, title, author, notes, when_read          
            from book, book_author, author, when_read                     
            where book.book_id=book_author.book_id and                    
            author.author_id=book_author.author_id and
            book.book_id=when_read.book_id and
title like "%s"
            """ %self.term

        output=execute(self.connection, sql)
        
        return output


if __name__ == '__main__':
    # test code:
    books = Books()
    term='dog'
    results = books.getBooks()
    kwdtest=books.getTerm(term)
    bNAtest=books.booksNotesAuthors()
    print "Num of books:", len(results)
    print kwdtest
    print bNAtest




