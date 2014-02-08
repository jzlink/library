#!/usr/bin/python
from database import *

class Books:
    '''Preside over Book records in the database'''

    def __init__(self):
        self.connection = getConnection()
        
    def getBooks(self):
        results = execute(self.connection, 
                          'select book_id, title from book')
        #book_id, title =  results[0]
        #return (book_id, title)
        return results
    
    def booksNotesAuthors(self):
        ''' Behavior: returns a list of all books, authors, and notes
        sorted by author'''

        sql= """select book.book_id, title, author, notes, when_read                                  
        from book, book_author, author, when_read                                    
        where book.book_id=book_author.book_id and                             
        author.author_id=book_author.author_id and
        book.book_id=when_read.book_id
        """

        output=execute(self.connection, sql)
        
        return output


if __name__ == '__main__':
    # test code:
    books = Books()
    results = books.getBooks()
    print "Num of books:", len(results)




