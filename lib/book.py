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
        if self.activity == 'edit':
            select = '''
concat(title) as Title,                                                     
concat(notes) as Notes,                                                     
published,                                                                  
concat(read_status.status) as 'Read Status',                                
concat(owner_status.status) as Ownership,                                   
concat(series.series) as 'Series Title',
concat(series.number) as  'Series No.',                       
concat(type) as Type,                                                       
concat(last_name) as 'Author Last Name',
concat(first_name) as 'Author First Name'
'''
        else:
            select ='''
concat(title) as Title,                                                     
concat(notes) as Notes,                                                     
published,                                                                  
concat(read_status.status) as 'Read Status',                                
concat(owner_status.status) as Ownership,                                   
concat(series.series,' #', series.number) as Series,                        
concat(type) as Type,                                                       
concat(last_name, ', ', first_name) as Author
'''
            
        sql = '''
select 
   %s
from
   book 
   inner join read_status on book.read_status_id= read_status.read_status_id
   left join owner_status on book.owner_status_id=owner_status.owner_status_id
   left join series on book.series_id=series.series_id 
   left join type on book.type_id=type.type_id
   left join book_author on book.book_id= book_author.book_id
   left join author on book_author.author_id=author.author_id 
where 
   book.book_id=%s''' % (select, self.book_id)


        result = execute(self.connection, sql)
        if not result:
            raise Exception('Unable to get book for book_id: %s' %self.book_id
                           )
        self.data = result[0]

    
def test():  
    book = Book(15)
    print book.data

if __name__ == '__main__':
    test()

        
