#!/usr/bin/python                                                                     
from database import *

class Search:

    def __init__(self):
        self.connection = getConnection()

    def setTerm(self, term):
        self.term=term

    def getTerm(self):
        return self.term

    def searchTitle(self):
        '''accepts keyword 'term', searches titles
        returns titles and associated info. of books that have term in the title
        '''
        self.term = term

        sql='''select title, book.book_id, author                                     
        from book, book_author, author                                                
        where title like '%demon%' and                                                
        book.book_id=book_author.book_id and                                          
        author.author_id=book_author.author_id;'''

        output=execute(self.connection, sql)
        return output


if __name__ == '__main__':
#test code                                                                            
    test= Search()
    test.setTerm('witch')
    TERM = test.getTerm()
    result= test.searchTitle()
    print TERM
    print result

