#!/usr/bin/env python

from datetime import datetime

from database import *

class WhenRead:
    'oversees all actions taken on the when_read table'

    def __init__(self):
        self.connection = getDictConnection() #connection return a dict
        self.conn = getConnection() #connection returns list


    def getWhenRead(self, book_id):
        ''' accepts a book id and 
        returns a list of list of datetime objects of when the book was read
        one list per date associated with each book id
        '''
        sql = '''select when_read
                 from when_read wr
                 join book b on wr.book_id = b.book_id
                 where b.book_id = %s
              ''' %book_id
    
        when = execute(self.conn, sql)
        
        return when

    def addWhenRead(self, book_id, date):
        ''' accepts a book_id date in mm/dd/yyy format
        adds the date and book_id pair to when_read table
        returns sucess message'''
        
        date = (datetime.strptime(date, '%m/%d/%Y')).date()
        date = date.isoformat()

        sql = "insert into when_read (book_id, when_read) values ('%s', '%s')"\
            % (book_id, date)

        add = execute(self.connection, sql)

        return '%s added to title' %date

    def removeWhenRead(self, book_id, date):
        ''' accepts a book_id date in mm/dd/yyy format
        removes the date and book_id pair from when_read table
        returns sucess message'''
        
        date = (datetime.strptime(date, '%m/%d/%Y')).date()
        date = date.isoformat()

        sql = "delete from when_read  where when_read = '%s' and book_id = %s"\
            % (date, book_id)

        add = execute(self.connection, sql)

        return '%s removed from title' %date

def test():
    test = WhenRead()
    getWhen = test.getWhenRead(335)
    add = test.addWhenRead(335, '06/05/2010')
    #remove = test.removeWhenRead(335, '06/05/2010')
    print getWhen

if __name__ == '__main__':
    test()
