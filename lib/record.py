#!/usr/bin/python 
from database import *

class Record:
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
   coalesce(notes,'') as notes,
   coalesce(published, '') as published,                          
   coalesce(read_status.status, '') as read_status,
   coalesce(owner_status.status, '') as owner_status,
   coalesce(series.series, '') as series,
   coalesce (series_num, '') as series_num,
   coalesce(type, '') as type,
   group_concat(distinct concat(last_name, ', ', first_name) order by last_name
      separator ' & ') as  author,
   group_concat(distinct when_read separator ' & ') as Date
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


    def updateRecord (self, update_dict):
        book = ['title', 'notes', 'published', 'owner_status_id', 'read_status_id', 'series_id', 'type_id', 'series_num']
        update_book = {}
        updates = []
        for key, value  in update_dict.items():
            if value:
                value = "'"+value+"'"
            else:
                value = 'NULL'
            if key in book:
                update_book.update({key: value})

        for item in update_book:
            sql = '''update book set %s = %s where book.book_id = %s''' %(item, update_book[item], self.book_id)
            result = execute(self.connection, sql)
            updates.append(item)
        message = "Fields "+ ', '.join(updates)+" have been successfully updated"
        return message
       
edits ={
'last_name': 'Mcguire', 
'type_id': '5', 
'series_name': None, 
'date': '2010-06-05', 
'first_name': 'Seanan', 
'title': 'A Local Habitation', 
'owner_status_id': '1', 
'notes': 'October Daye bk. 2', 
'series_num': None, 
'published': '1', 
'read_status_id': '1'
}
    
def test():  
   book = Book(335, 'view')
 # print book.data
   update= book.updateRecord(edits)
   print update

if __name__ == '__main__':
    test()

        
