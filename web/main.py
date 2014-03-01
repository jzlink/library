#!/usr/bin/env python

import cgi
import cgitb
cgitb.enable()
#enables colored error messages to appear in browser. 

from books import Books
#from book class import book functions

form = cgi.FieldStorage()

term= form.getvalue('term', '')
#sets term to 'term'  or else defaults 'term' to empty string 

# build report body:
books = Books()
results = books.retrieveCoreData(term)

# build html table
table = '<table border="1" cellpadding="3" cellspacing="0">\n'
table += '<tr><th>#</th><th>Title</th><th>Author</th><th>Notes</th><th>Date</th></tr>\n'

i=1
for (book_id, title, author, notes, when_read) in results:
    table += ' <tr><td>%d</td><td><a href=\"detail.py?book_id=%d">%s</td><td>%s</td><td>%s</td><td><nobr>%s</nobr></td></tr>\n' %(i, book_id, title,author,notes, when_read)
    i=i+1
table += '</table>\n'


# Output HTML
print 'Content-Type: text/html\n'

print "<html>"
print "<h3>Books, Authors, and Notes</h3>"

print """
<form method= 'GET' action= " "> 
Search Titles For: <input type='text' name ='term'/>
<input type =  'submit' />
</form>"""
#generates from that accepts keyword search term

if term:
    print 'Search term is %s' %term

print table
print "</html>"
