#!/usr/bin/python

import MySQLdb
from  database import *

#cursor=getConnection()

class Author:

    def countAuthors(self):
        '''Behavior: Returns the number of authors in the library'''

        cursor=getConnection()

        sql='select count(author_id) from author'

        output=execute(cursor,sql)
        
        cursor.close()

        return output
        
       
    def booksByAuthor(self):
        '''Behavior: returns a list of all authors by name and all of the
        books they have in the database
        '''
        cursor=getConnection()
        
        sql= """select author, count(book_id)
        from book_author inner join author
        on author.author_id=book_author.author_id
        group by author
        """

        output=execute(cursor,sql)
        
        cursor.close()

        return output


