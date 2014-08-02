#!/usr/bin/python 

from database import *

edits ={
'author.last_name': 'Mcguire', 
'book.type_id': '5', 
'series.series_name': 'NULL', 
'when_read.date': '2010-06-05', 
'author.first_name': 'Seanan', 
'book.title': 'A Local Habitation', 
'book.owner_status_id': '1', 
'book.notes': 'October Daye bk. 2', 
'book.series_num': 'NULL', 
'book.published': '1', 
'book.read_status_id': '1'
}

book_id = 335

connection = getDictConnection()
for key, value in edits.items():
    x = key.find('.')
    table = key[0:x]
    if table == 'book':
        sql = '''
          update %s 
          set %s = %s
          where book.book_id = %s
          '''%(table, key, value, book_id)
    
    if table == 'author':
        sql1 = 'select author_id from book_author where book_id =%s''' %book_id
        result = execute(connection, sql1)
        y = result[0]
        sql = '''
          update %s 
          set %s = %s
          where book.book_id = %s
          '''%(table, key, value, y)
        print result['author_id']
