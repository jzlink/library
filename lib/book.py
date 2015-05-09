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

    def updateBook(self, formDict):
        '''accepts a dictionary of column:value pairs 
        'book_id' must be an included column
        call the getDiff method to check if an update should be made
        if an update is necessary update the DB
        return dictionary of changed columns and their new values
        '''
        updates = {}
        book_id = formDict['book_id']

        diffs = self.getDiff(formDict)

        if len(diffs) > 0:
            for column in diffs:
                value = formDict[column]

                #check metadata to see what type it is
                varType = self.columns[column][0]['type']
        
                if varType == 'int' and value == '':
                    value = 'NULL'
                else:
                    value ='"'+ str(value)+'"'
                        
                updates[column]= value
            
            setClause = ''
        
            count = 0
            for column in updates:
                setClause += column
                setClause += " = %s" % updates[column]
                count +=1
                if count < len(updates):
                    setClause += ', '

            sql ='update book set %s where book_id = %s'\
                % (setClause, book_id)
            results = execute(self.connection, sql)

        return setClause

    def getDiff(self, formDict):
        '''accepts a formDict that includes book_id
        checks which, if any, form values are different from the current value
        in the DB. Retuns list of values that differ.
        '''

        diffs = []

        sql = 'select * from book where book_id = %s' % (formDict['book_id'])
        currentRec = execute(self.connection, sql)

        #for each column, test it against the current value
        for column in formDict:

            currentVal = str(currentRec[0][column])
            if currentVal == 'None':
                currentVal = ''

            if formDict[column] != currentVal:
                diffs.append(column)
            
        #return diffs, formDict, currentRec
        return diffs
    
def test():

    testDict = {'book_id': '12', 'title': 'Dead Unitl Dark', 'notes': '',
                'published': '1', 'owner_status_id': '1',
                'read_status_id': '1', 'type_id': '1', 
                'series_id': '4','series_num': '1'}

    test = Book()
    #print  test.getDiff(testDict)
    print test.updateBook(testDict)


if __name__ == '__main__':
    test()


