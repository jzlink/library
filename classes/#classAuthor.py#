#!/usr/bin/python

import MySQLdb

library= MySQLdb.connect('localhost', 'jlink', 'eggplant', 'library')
cursor=library.cursor()

class Author:

    def countAuthors(self):
        '''Behavior: Returns the number of authors in the library'''

        sql='select count(author_id) from author'
        cursor.execute(sql)

        number=cursor.fetchone()
        answer= number[0]

        print "There are %s authors in the library." %(answer)
        
       

    def booksByAuthor(self):
        '''Behavior: returns a list of all authors by name and all of the
        books they have in the database
        '''


        sql= """select author, count(book_id)
        from book_author inner join author
        on author.author_id=book_author.author_id
        group by author
        """
        cursor.execute(sql)

        template= '{0:40}|{1:5}'
        print template.format ("Author", "Books Read")


        for (author, count) in cursor.fetchall():
            print template.format(author,count)


