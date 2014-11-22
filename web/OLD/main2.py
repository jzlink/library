#!/usr/bin/env python

import cgi

#enables color coded error messages
import cgitb
cgitb.enable()

from books import Books
from htmltable import HtmlTable
from utils import date2str

# process form inputs
form = cgi.FieldStorage()
term = form.getvalue('term', '')
clear= form.getvalue('clear')
order_by= form.getvalue('order_by', '')

# build report body:
books = Books()
results = books.retrieveCoreData(term, order_by)

# build html table
table = HtmlTable(border=1, cellpadding=3)

# table header
header = ['#',
          '<a href= "main2.py?order_by=title">Title</a>',
          '<a href= "main2.py?order_by=author">Author</a>',
          '<a href= "main2.py?order_by=notes">Notes</a>',
          '<a href= "main2.py?order_by=when_read">Date</a>']
table.addHeader(header)

# table body
i = 0
for (book_id, title, author, notes, when_read) in results:
    i += 1
    href = '<a href="detail.py?book_id=%d">%s' % (book_id, title)
    date = '<nobr>%s</nobr>' % date2str(when_read)
    table.addRow([i, href, author, notes, date])

# Output HTML
print 'Content-Type: text/html\n'

print "<html>"
print """
<head>
<title> Read A Book! </title>
<link href="css/main.css" rel="stylesheet" type="text/css">
</head>"""

print "<body>"
print "<h3>Books, Authors, and Notes</h3>"

print """
<form method= 'GET' action= "main2.py "> 
Search Titles For: <input type='text' name ='term' value='%s'/>
table.addHeader(['#','<input type= 'submit' name= 'order_by' value= 'Title','<a href= "main.py?order_by=author">Author','<a href= "main.py?order_by=notes">Notes','<a href= \
"main.py?order_by=when_read">Date'])
<input type = 'hidden' name= 'order_by' value='title'>
<input type =  'submit' />
<input type = "submit" name= 'clear'  value = "Clear">
</form>""" %term

if clear:
    term=''

if term:
    print 'Search term is %s' %term

print table.getTable()
print 'order_by: %s' %order_by
print "</body>"
print "</html>"
