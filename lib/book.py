#!/usr/bin/env python

from database import *
from utils import loadYaml

class Book():
    'oversees all actions taken on the book table'

    def __init__(self):
        self.connection = getDictConnection()
        self.columns = loadYaml('columns')

    def updateBook(self, formDict):
        updates = {}
        book_id = formDict['book_id']
        for column, value in formDict.items():
            if column in self.columns:
                record_table = self.columns[column][0]['from']
                edit = self.columns[column][0]['editable']

                if record_table == 'book' and edit == 'T':
                    update = self.getDiff(book_id, column, value)
                    if update:
                        if type(value) == str:
                            value = '"%s"' %value
                            sql = \
                            'update book set %s = %s where book.book_id = %s'\
                                % (column, value, book_id)
                            results = execute(self.connection, sql)
                            updates[column]= value

        return updates

    def getDiff(self, book_id, column, value):
        different = True
        sql = 'select %s from book where book_id = %s' % (column, book_id)
        results = execute(self.connection, sql)
        bookVal = str(results[0][column])

        if bookVal == None or bookVal == 'NULL':
            bookVal = ''

        if bookVal == value:
            different = False

        return different, value, bookVal


def test():
    testDict = {'book_id': 328 , 'title': 'Good Omens', 'notes': 'Re-read, I remember it being better'}

    test = Book()
    print  test.getDiff(328, 'notes', 'Re-read, I remember it being better')
#    updates = test.updateBook(testDict)
#    print "Updated the following columns: %s" %updates

if __name__ == '__main__':
    test()


