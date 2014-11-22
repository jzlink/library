#!/usr/bin/env python  

from database import *
from libraryHTML import *

book_id = 335
connection = getDictConnection()
sql = 'select when_read from when_read where book_id = %s' %book_id
results = execute(connection, sql)

html = LibraryHTML(book_id, 'edit')

for time in results:
    print time['when_read']

print results


