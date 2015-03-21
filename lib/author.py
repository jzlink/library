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

    def getAsAutoCDict(self):
        '''Return all author records as a list of dicts with key, values
           of last name, first name, if as in:
           [{last_name:Pratchett, first_name:Terry, author_id:10},
           {last:smith, first:john, id:4}, etc.]
        '''
        sql = '''select author_id as value,
                        first_name,
                        last_name,
                        concat(last_name, ', ', first_name) as label
                 from author'''

        authors = execute(self.connection, sql)

        return authors

    def updateAuthor(self, formDict):
        '''accepts dict from edit author module
        checks is values need to be added to DB and calls functions to
        add them if necessary. Returns list of updated fields'''

        updates = {}
        author_id = formDict['author_id']
        book_id = formDict['book_id']

        if author_id:
            sql = '''select ba_id  from book_author 
                      where author_id = %s and book_id = %s
                 ''' % (author_id, book_id)

            results = execute(self.connection, sql)
            
            if 'ba_id' not in results:
                add = self.addBookAuthor(book_id, author_id)
                updates['author_id'] = author_id

        if author_id == '' and \
                (formDict['first_name'] !='' or\
                formDict['last_name'] != ''):

            name_sql = ''' select author_id from author
              where first_name = '%s' and last_name = '%s'
              '''%(formDict['first_name'], formDict['last_name'])

            results = execute(self.connection, name_sql)
            
            if len(results) < 1:
                add = self.addNewAuthor(formDict['last_name'],\
                                        formDict['first_name'])

                updates['first_name'] = formDict['first_name']
                updates['last_name']  = formDict['last_name']

                sql = '''select max(author_id) as author_id from author'''

                results = execute(self.connection, sql)

            add = self.addBookAuthor(book_id, results[0]['author_id'])
            updates['author_id'] = results[0]['author_id']    
            
        return updates

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
 #   getAuthors = test.getBookAuthor(328)
   # authordict =test.getAsDict()
    testDict = {'author': 'Martin, George R. R.', 'author_id': '',\
        'book_id': '131', 'first_name': 'Rex', 'last_name': 'T'}

    print test.updateAuthor(testDict)

if __name__ == '__main__':
    test()
