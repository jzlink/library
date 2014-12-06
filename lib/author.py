#!/usr/bin/env python

from database import *

class Author:
    'oversees all actions taken on the author table'

    def __init__(self):
        self.connection = getDictConnection()

    def getBookAuthor(self, book_id):
        ''' accepts a book id and 
        returns a list of dicts of author first and last names
        one dict per author associated with each book id
        '''
        sql = '''select last_name, first_name, a.author_id
                 from author a
                 join book_author ba on a.author_id = ba.author_id
                 where ba.book_id = %s
              ''' %book_id
    
        authors = execute(self.connection, sql)
        
        return authors

    def getCatAuthors(self):
        
        sql = '''select author_id, concat(last_name, ', ', first_name)
                 from author'''

        authors = execute(self.connection, sql)

        return authors

    def addBookAuthor(self, book_id, author_id):
        ''' accepts a book_id and author_id
        updates book_author table to include that author on that book
        returns sucess message'''

        sql = ''' insert into book_author (book_id, author_id)
                  values ('%s', '%s')
              ''' % (book_id, author_id)

        update = execute(self.connection, sql)

        return 'author added to book'

    def removeBookAuthor(self, book_id, author_id):
        ''' accepts a book_id and author_id
        removes that book/author pair from the table
        returns sucess message'''

        sql = '''delete from book_author 
                 where author_id = %s and book_id = %s
                 ''' % (author_id, book_id)

        update = execute(self.connection, sql)

        return 'author removed from title'

    def addNewAuthor(self, lastName, firstName):
        '''accepts an authors last and first name
        adds this new person to the author table
        returns sucess message'''
        
        sql = '''insert into author (last_name, first_name)
                 values ('%s', '%s')''' %(lastName, firstName)

        addtion = execute(self.connection, sql)
        
        return "Author %s %s added to Database" %(firstName, lastName)

def test():
    test = Author()
    #addAuthor = test.addNewAuthor('Eager', 'Edward')
    #add = test.addBookAuthor(328, 224)
    #remove = test.removeBookAuthor(328,224)
    getAuthors = test.getBookAuthor(328)
    print getAuthors

if __name__ == '__main__':
    test()
