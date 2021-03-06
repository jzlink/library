#!/usr/bin/env python

import cgi

#enables color coded error messages
import cgitb
cgitb.enable()

from books import Books

from htmltable import HtmlTable

# process form inputs
form = cgi.FieldStorage()
term = form.getvalue('term', '')
order_by= form.getvalue('order_by', '')

# build report body:
books = Books()
results = books.retrieveCoreData(term, order_by)

title= '=title'

# build html table
table = '<table border="1" cellpadding="3" cellspacing="0">\n'
table += """
<tr>
<th>#</th>
<th><form> <input type = "submit" name = 'order_by' value = 'Title'/></form></th>
<th><a href= "main.py?order_by=author">Author</th>
<th><a href= "main.py?order_by=notes">Notes</th>
<th><a href= "main.py?order_by=when_read">Date</th>
</tr>\n"""

i=1
for (book_id, title, author, notes, when_read) in results:
    table += """
<tr>
<td>%d</td>
<td><a href=\"detail.py?book_id=%d">%s</td>
<td>%s</td>
<td>%s</td>
<td><nobr>%s</nobr></td>
</tr>\n""" %(i, book_id, title,author,notes, when_read)
    i=i+1
table += '</table>\n'


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
<form method= 'GET' action= "main.py "> 
Search Titles For: <input type='text' name ='term' value='%s'/>
<input type =  'submit' />
</form>""" %term 

if term:
    print 'Search term is %s' %term

print table
print "</body>"
print "</html>"
