#!/usr/bin/env python

import cgi

#enables color coded error messages
import cgitb
cgitb.enable()

from books import Books
from htmltable import HtmlTable
from utils import date2str

### PROCESS INPUTS

form = cgi.FieldStorage()
term = form.getvalue('term', '')
term2 = form.getvalue('term2', '')
order_by= form.getvalue('order_by', '')


### START HTML

print 'Content-Type: text/html\n'
print "<html>"
print """
<head>
<title> Read A Book! </title>
<link href="css/main.css" rel="stylesheet" type="text/css">
</head>"""
print "<body>"


### TITLE

print "<h3>Books, Authors, and Notes</h3>"

### SEARCH SECTION

print """
<form method="POST" action="main.py" name="form1"> 
Search Titles For: 

<input type='textfield' name ='term' value='%s'/>
<input type='submit' value='submit'/>
<input type='button' value='clear' 
       onclick="javascript:document.form1.term.value=''; 
                document.form1.submit();"/>
<input type='hidden' name='order_by' value='%s'/>
</form>""" % (term, order_by)

if term:
    print 'Search term is %s' %term


### TABLE OF BOOKS

books = Books()
results = books.retrieveCoreData(term, order_by)

# build html table
table = HtmlTable(border=1, cellpadding=3)

# table header
header = ['#']
for field, name in [['title'    , 'Title'],
                    ['author'   , 'Author'],
                    ['notes'    , 'Notes'],
                    ['when_read', 'Date']]:
    sortflag =''
    if field == order_by:
        sortflag = ' ^'
    js =  "document.form1.order_by.value='%s';" % field
    js += "document.form1.submit();"
    h = '<a onclick="javascript:%s">%s%s</a>' % (js, name, sortflag)
    header.append(h)
table.addHeader(header)

# table body
i = 0
activity = 'view'
for (book_id, title, author, notes, when_read) in results:
    i += 1
    href = '<a href="detail.py?book_id=%d&activity=%s">%s' % (book_id, activity, title)
    date = '<nobr>%s</nobr>' % date2str(when_read)
    table.addRow([i, href, author, notes, date])

print table.getTable()

### FOOTER

print "</body>"
print "</html>"
