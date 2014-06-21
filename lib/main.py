#!/usr/bin/env python                                                           

from books import Books
#from query import Query

# build report body:                                                           
books = Books()
results = books.booksNotesAuthors()

#query= Query()
#catalog = query.getData('main')
# build html table                                                              
table = '<table border="1" cellpadding="3" cellspacing="0">\n'
table += ' <tr><th>Title</th><th>Author</th><th>Notes</th></tr>\n'
for r in results:
    table += ' <tr><td>%s</td><td>%s</td>td>%s</td></tr>\n' % r
table += '</table>\n'

# Output HTML                                                                   
print 'Content-Type: text/html\n'

print "<html>"
print "<h3>Books, Authors, and Notes</h3>"
table += ' <tr><th>Title</th><th>Author</th><th>Notes</th></tr>\n'
for r in results:
    table += ' <tr><td>%s</td><td align="right">%s</td></tr>\n' % r
table += '</table>\n'

# Output HTML                                                                   
print 'Content-Type: text/html\n'

print "<html>"
print "<h3>Books by Author</h3>"
print table
print "</html>"
