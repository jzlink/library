#!/usr/bin/env python

'''Display Book Record Details'''

# call like this: http://julia-link.com/detail.py?book_id=50

import cgi
import cgitb
cgitb.enable()

from book import Book
from utils import date2str

# get book_id 
form = cgi.FieldStorage()
if 'book_id' not in form:
    book_id = 1
else:
    book_id = form['book_id'].value

if 'activity' not in form:
    activity = 'view'
else:
    activity = form['activity'].value 

# build report body:

book = Book(book_id, activity)

# build html table
table = '<table border="1" cellpadding="3" cellspacing="0">\n'
table += '<tr><th>Column</th><th>Value</th></tr>\n'


for key, value in book.data.items():

    if value == None:
        value= 'Unknown'

    #Special Handeling for binary field published
    if key =='published':
        key = 'Published'
    if key == 'Published' and value == 1:
        value = 'Yes'
    if key == 'Published' and value == 0:
        value = 'No'
    
    #Special handeling for date output
    if key == 'when_read':
        key= 'Date Read'
        value =date2str(value)
    
    table += ' <tr><td>%s</td><td>%s</td></tr>\n' % (key, value)
    
table += '</table>\n'

foo= 'edit'

# Output HTML
print 'Content-Type: text/html\n'

print "<html>"
print "<h3>Book Record</h3>"
print table
print '''
<a href =  "edit.py?book_id=%s&activity=%s"> Edit Record </a>
'''% (book_id, foo)
print "</html>"
