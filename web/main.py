#!/usr/bin/env python

import cgi

#enables color coded error messages
import cgitb
cgitb.enable()

from pprint import pprint

from database import *
from metadata import Metadata
from query import Query
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

print "<header role = 'banner'>"
##Header
print "<h1>Julia's Library</h1>"

##Search Section
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

where = ''
if term:
    print 'Search term is %s' %term
    kwd = "'%" + term + "%'"
    where = "title like %s" %kwd


##Add Book Button
print '''
    <input type = "button" onClick = 
      "location.href='detail.py?book_id=0&activity=add'" value = "Add Record">
'''
#connection = getConnection()

#results = execute (connection, "select auto_increment
#from information_schema.TABLES
#where table_name = 'book'")



print "<div id = 'header-fixed'>"
print "</header>"
print "</div>"

### TABLE OF BOOKS

query= Query()
results = query.getData('main', where, order_by)

metadata = Metadata()
data = metadata.interrogateMetadata('main', 'display')
#ordered_cols = data['ordered_cols']
display_names = data['col_attributes'] 
#ordered_cols.remove('book_id') #we don't want book_id to be a column heading

# build html table
table = HtmlTable(border=1, cellpadding=3)

# table header

header = ['#']

#use the display_name list to build a header that enables sorting   
for field, name in display_names:
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

for rec in results: 
    i += 1
    href = '<a href="detail.py?book_id=%d&activity=%s">%s'% (rec['book_id'], activity, rec['title'])
    table.addRow([i, href, rec['author'], rec['notes'], rec['date']])

print table.getTable()

### FOOTER

print "</body>"
print "</html>"

