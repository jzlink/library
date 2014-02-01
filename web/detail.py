#!/usr/bin/env python

'''Display Book Record Details'''

from book import Book

BOOK_ID = 7 # pass this in as arg later.

# build report body:
book = Book(BOOK_ID)

# build html table
table = '<table border="1" cellpadding="3" cellspacing="0">\n'
table += '<tr><th>Column</th><th>Value</th></tr>\n'

#data = {}
#data['title'] = book.data.title
#data['Status'] = book.data.owner_status.status
#data['Status'] = book.data.owner_status

for key, value in book.data.items():
    column_name = key.replace('_', ' ').title()
    table += ' <tr><td>%s</td><td>%s</td></tr>\n' % (column_name, value)
table += '</table>\n'


# Output HTML
print 'Content-Type: text/html\n'

print "<html>"
print "<h3>Books, Authors, and Notes</h3>"
print table
print "</html>"
