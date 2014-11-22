#!/usr/bin/env python

from database import *

class Series:
    'oversees all actions taken on the series table'

    def __init__(self):
        self.connection = getDictConnection()

    def getSeries(self, book_id):
        ''' accepts a book id and 
        returns the series id and series name of any series associated 
        with the book. If no series are associated returns false
        '''
        sql = '''select s.series_id, s.series
                 from series s
                 join book b on b.series_id = s.series_id
                 where book_id = %s
              ''' % book_id
    
        series = execute(self.connection, sql)
        
        if len(series) < 1:
            series = False

        return series

    def addNewSeries(self, series):
        '''accepts a series name
        adds this name to the series table
        returns sucess message'''
        
        sql = '''insert into series (series)
                 values ('%s')''' % (series)

        addtion = execute(self.connection, sql)
        
        return "Series %s  added to Database" %(series)

def test():
    test = Series()
    getSeries = test.getSeries(1)
    addSeries = test.addNewSeries('Millennium Series')
    print addSeries

if __name__ == '__main__':
    test()
