#!/usr/bin/python                                                                     
from database import *

class Search:
    '''enables various searches of the database'''

    def __init__(self):
        self.connection = getDictConnection()

    def setTerm(self, term):
       '''accepts term and returns term with % to either end of it for use in query'''
       self.term=term
       self.term= "%" + self.term + "%"
    
    def reveal(self):
        '''behavior: prints what term is for tesing purposes'''
        print "Term is: %s" % self.term

    def searchTitle(self):
        '''searches titles using self.term
        returns dictonary of titles and associated info. of books that 
        have term in the title'''

        sql='''select title, book.book_id, author                                     
        from book, book_author, author                                                
        where title like "%s" and                                                
        book.book_id=book_author.book_id and                                          
        author.author_id=book_author.author_id;''' % self.term

        output=execute(self.connection, sql)
        return output


if __name__ == '__main__':
#test code code works if output shows "Term is: %witch% and
#books having witch in the title                                                          
    test= Search()
    test.setTerm('witch')
    test.reveal()
    result= test.searchTitle()
    print result
