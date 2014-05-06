#!/usr/bin/python 
from database import *

class Book:
    '''Preside over a single book record in the database'''

    def __init__(self, book_id, activity):
        '''Given a book_id fetch the book data'''
        self.book_id = book_id
        self.activity = activity
        self.connection = getDictConnection()
        self.getData()

    def getData(self):
        sql = '''
select 
   title,
   notes,
   published,                                                                  
   read_status.status,
   owner_status.status,
   series.series,
   series_num,
   type,
   last_name,  
   first_name,
   when_read.when_read
from
   book 
   inner join read_status on book.read_status_id= read_status.read_status_id
   left join owner_status on book.owner_status_id=owner_status.owner_status_id
   left join type on book.type_id=type.type_id
   left join book_author on book.book_id= book_author.book_id
   left join author on book_author.author_id=author.author_id
   left join when_read on book.book_id= when_read.book_id
   left join series on book.series_id=series.series_id
where 
   book.book_id=%s''' % (self.book_id)


        result = execute(self.connection, sql)
        if not result:
            raise Exception('Unable to get book for book_id: %s' %self.book_id
                           )
        self.data = result[0]


    def editRecord (self, editDict):
        booksql ='''
update book
set series_num = %s
where book_id = %s
''' % (editDict['series_num'], self.book_id) 

        
        sql = '''
update book
set 
   title = "%s",
   notes = "%s",
   published = %s,
   read_status_id = %s,
   owner_status_id = %s,
   type_id = %s,
   series_num = %s
where book_id = %s
''' % (editDict['title'], 
       editDict['notes'],
       editDict['published'],
       editDict['read_status.status'], 
       editDict['owner_status.status'], 
       editDict['type'], 
       editDict['series_num'], 
       self.book_id)

        try:
           # print "booksql:", booksql
            print 'sql:', sql
            result = execute(self.connection, sql)
            return "OK"

        except Exception, e:
            #raise
            return "ERROR: %s" % e
       
edits = {
        'read_status.status'  : 1,
        'first_name'          : 'Christopher',
        'last_name'           : 'Moore',
        'title'               : 'Practical Demonkeeping',
        'series.series'       : '',
        'notes'               : '',
        'series_num'          : 'NULL', 
        'owner_status.status' : 1,
        'published'           : 1,
        'type'                : 1,
        'when_read.when_read' : 2004-06-01
        }
    
def test():  
   book = Book(1, 'view')
 # print book.data
   print book.editRecord(edits)
   

if __name__ == '__main__':
    test()

        
