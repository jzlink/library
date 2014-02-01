#!/usr/bin/env python                                                           

from books import Books
#from book class import book functions                                                    

# build report body:                                                            
books = Books()
results = books.booksNotesAuthors()

# build html table                                                              
table = '<table border="1" cellpadding="3" cellspacing="0">\n'
table += '<tr><th>#</th><th>Title</th><th>Author</th><th>Notes</th></tr>\n'

i=1
for (title, author, notes) in results:
    table += ' <tr><td>%d<d/td><td>%s</td><td>%s</td><td>%s</td></tr>\n' %(i, title,author,notes)
    i=i+1
table += '</table>\n'


# Output HTML                                                                   
print 'Content-Type: text/html\n'

print "<html>"
print "<h3>Books, Authors, and Notes</h3>"
print table
print "</html>"
