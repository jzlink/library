#!/usr/bin/env python

from database import *
from utils import loadYaml

class Book():
    'oversees all actions taken on the book table'

    def __init__(self):
        self.connection = getDictConnection()
        self.columns = loadYaml('columns')


    def addBook(self):
        addSQL = 'insert into book (title) values ("STARTER")'
        addDummy = execute(self.connection, addSQL)

        findSQL = 'select book_id from book where title = "STARTER"'
        book_id = execute(self.connection, findSQL)

        return book_id[0]['book_id']

    def updateColumn(self, book_id, column, value):
        '''accepts a book_id, column in the book table and a value
        updates the column with the value
        return success message
        '''

        sql ='''update book set %s = %s where book_id = %s
                       ''' % (column, value, book_id)
        results = execute(self.connection, sql)

        return '%s updated to %s' %(column, value)

    def updateBook(self, formDict):
        '''accepts a dictionary of column:value pairs 
        'book_id' must be an included column
        checks if each column in editable if it is
        call the getDiff method to check if an update should be made
        if an update is necessary update the record
        return dictionary of changed columns and thier new values
        '''
        updates = {}
        book_id = formDict['book_id']
        for column, value in formDict.items():
            #check metadata to see if column can be edited and what type it is
            edit = self.columns[column][0]['editable']
            varType = self.columns[column][0]['type']
        
            #if it can be edited preform a getDiff
            if edit == 'T':
               # if value == '':
               #     value = None
                update = self.getDiff(book_id, column, value)

                #if getDiff comes back positve update the record
                if update:
                    if varType == 'int' and value == '':
                        value = 'NULL'
                    else:
                        value ='"'+ str(value)+'"'
                        
                    self.updateColumn(book_id, column, value)
                    updates[column]= value

        return updates

    def getDiff(self, book_id, column, value):
        '''accepts a book ID, column in the book table and a column value
        checks if the accepted value is different from the current value for
        the column in the DB. Retuns true or false if the values differ.
        '''
        different = True

        sql = 'select %s from book where book_id = %s' % (column, book_id)
        results = execute(self.connection, sql)
        bookVal = str(results[0][column])
        if bookVal == 'None':
            bookVal = ''

        if bookVal == value:
            different = False
            
        #return different, value, bookVal
        return different
    

def test():
    testDict = {'book_id': '335', 'notes': 'bk. 3', 'owner_status_id': 'None', 'published': '1', 'read_status_id': '1', 'series_num': '', 'title': 'Destiny', 'type_id': 'None'}
    test = Book()
   # print  test.getDiff(241, 'series_num', None)
    print test.updateBook({'series_num': ''})


if __name__ == '__main__':
    test()


