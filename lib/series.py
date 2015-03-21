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
        returns series_id of new series name'''
        
        sql = '''insert into series (series)
                 values ('%s')''' % (series)

        addtion = execute(self.connection, sql)
        
        IDsql = "select series_id from series where series = ('%s')" %series
        results = execute(self.connection, IDsql)
        series_id = results[0]['series_id']
        
        return series_id

    def getAsAutoCDict(self):
        '''Return all series records as a dict with key, values
           of id and name as value and lable suitable for auto complete
           function '''

        sql = 'select series_id as value, series as label from series'
        results = execute(self.connection, sql)

        return results

    def updateSeries(self, formDict):
        ''' update series by checking if the given series is in the DB yet,
        adding it if it is not, then adding the series to the book, return
        success message'''
        #get series_id
        series_id = formDict['series_id']
        series_name = formDict['series']
       
        #if there is no series ID and there is a series name one of two things
        #could be happening: 1- the series was the default name (already
        #assigned to the book), in which case do nothing OR the series name is
        # new and needs to be added to the DB, in which case add it

        #check if series name is in the DB or not
        if series_id == '' and series_name !='':
            sql = 'select series_id from series where series = ("%s")'\
                %series_name
            results = execute(self.connection, sql)
            if results:
                series_id = results[0]['series_id']
            else:
               series_id =  self.addNewSeries(series_name)

        #check if the series_id and book_id are already paired
        sql = 'select series_id from book where book_id = ("%s")'\
            %formDict['book_id']
        results = execute(self.connection, sql)

        #if they are pass, else add them.
        if results[0]['series_id'] == series_id:
            pass
        else:
            sql = 'update book set series_id = ("%s") where book_id = ("%s")'\
                %(series_id, formDict['book_id'])
            
            results = execute(self.connection, sql)
            x = 'updated series_id in book table'
        return 'update activate'

def test():
    test = Series()
    testDict = {'book_id': 522, 'series_id':'', 'series_name': 'Twelve Houses'}
#    getSeries = test.getSeries(1)
#    addSeries = test.addNewSeries('Millennium Series')
    print test.updateSeries(testDict)

if __name__ == '__main__':
    test()
