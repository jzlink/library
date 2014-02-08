#!/usr/bin/env python

from books import Books
#from book class import book functions

# build report body:
books = Books()
results = books.booksNotesAuthors()

# build html table
table = '<table border="1" cellpadding="3" cellspacing="0">\n'
table += '<tr><th>#</th><th>Title</th><th>Author</th><th>Notes</th><th>Date</th></tr>\n'

i=1
for (book_id, title, author, notes, when_read) in results:
    table += ' <tr><td>%d</td><td><a href=\"detail.py?book_id=%d">%s</td><td>%s</td><td>%s</td><td>%s</td></tr>\n' %(i, book_id, title,author,notes, when_read)
    i=i+1
table += '</table>\n'


# Output HTML
print 'Content-Type: text/html\n'

print "<html>"
print "<h3>Books, Authors, and Notes</h3>"
print table
print "</html>"
