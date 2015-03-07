#!/usr/bin/env python

from database import *
from utils import loadYaml

class Book():
    'oversees all actions taken on the book table'

    def __init__(self):
        self.connection = getDictConnection()
        self.columns = loadYaml('columns')


    def addBook(self, formDict):
        addSQL = 'insert into book (title) values ("STARTER")'
        addDummy = execute(self.connection, addSQL)

        findSQL = 'select book_id from book where title = "STARTER"'
        book_id = execute(self.connection, findSQL)

        formDict['book_id'] = book_id[0]['book_id']

        update = self.updateBook(formDict)

        return book_id[0]['book_id']

    def updateBook(self, formDict):
        updates = {}
        book_id = formDict['book_id']
        for column, value in formDict.items():
            edit = self.columns[column][0]['editable']
            varType = self.columns[column][0]['type']
        
            if edit == 'T':
                if value == '':
                    value == None
                update = self.getDiff(book_id, column, value)
                
                if update and value:
                    if varType == 'string':
                        value = str(value)
                    if varType == 'int':
                        value = int(value)
                        
                    sql ='update book set %s = %s where book.book_id = %s'\
                        % (column, value, book_id)
                    results = execute(self.connection, sql)
                    updates[column]= value

        return updates

    def getDiff(self, book_id, column, value):
        different = True

        sql = 'select %s from book where book_id = %s' % (column, book_id)
        results = execute(self.connection, sql)
        bookVal = str(results[0][column] or '')

        if bookVal == value:
            different = False
            
        #return different, value, bookVal
        return different
    

def test():
    testDict = {'book_id': 328 , 'title': 'Good Omens', 'notes': 'Re-read, I remember it being better'}

    test = Book()
    print  test.getDiff(328, 'series_num', '')
#    updates = test.updateBook(testDict)
#    print "Updated the following columns: %s" %updates

if __name__ == '__main__':
    test()


