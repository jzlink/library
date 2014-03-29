#!/usr/bin/python

import MySQLdb
from  database import *

#cursor=getConnection()

class Author:

    def __init__(self):
        self.cursor = getConnection()

    def countAuthors(self):
        '''Behavior: Returns the number of authors in the library'''

        sql='select count(author_id) from author'

        output=execute(self.cursor, sql)[0]
        
        return output
        
       
    def booksByAuthor(self):
        '''Behavior: returns a list of all authors by name and the number of
        books they have in the database
        '''
        
        sql= """select concat(author.last_name, ', ', author.first_name) as author, count(book_id)
        from book_author inner join author
        on author.author_id=book_author.author_id
        group by author
        """

        output=execute(self.cursor,sql)
        
        return output


