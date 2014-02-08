#!/usr/bin/env python

'''Display Book Record Details'''

# call like this: http://julia-link.com/detail.py?book_id=50

import cgi

from book import Book

# get book_id 
form = cgi.FieldStorage()
if 'book_id' not in form:
    book_id = 1
else:
    book_id = form['book_id'].value


# build report body:

book = Book(book_id)

# build html table
table = '<table border="1" cellpadding="3" cellspacing="0">\n'
table += '<tr><th>Column</th><th>Value</th></tr>\n'

#data = {}
#data['title'] = book.data.title
#data['Status'] = book.data.owner_status.status
#data['Status'] = book.data.owner_status

for key, value in book.data.items():
    column_name = key.replace('_', ' ').title()

    # spec. handling for Owner status lookup data
    if key == 'owner_status_id':
        column_name = 'Owner Status'
        value = book.owner_status['status']

    table += ' <tr><td>%s</td><td>%s</td></tr>\n' % (column_name, value)
    
table += '</table>\n'


# Output HTML
print 'Content-Type: text/html\n'

print "<html>"
print "<h3>Books, Authors, and Notes</h3>"
print table
print "</html>"
