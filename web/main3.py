#!/usr/bin/env python

import cgi

#enables color coded error messages
import cgitb
cgitb.enable()

from pprint import pprint

from loadyaml import LoadYaml
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


### TITLE

print "<h3>Books, Authors, and Notes</h3>"

### SEARCH SECTION

print """
<form method="POST" action="main3.py" name="form1"> 
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
    
### TABLE OF BOOKS

query= Query()
results = query.getData('main', where, order_by)

loadyaml = LoadYaml()
columns = loadyaml.loadYaml('columns')
pages = loadyaml.loadYaml('pages')

# build html table
table = HtmlTable(border=1, cellpadding=3)

# table header
ordered_header = ['#']

# make a dictionary of all of the columns and their display names needed for
# the table header. Remove 'book_id' since we don't want that as a column

col_order= []
for item in pages['main']:
    col_order.append(item)
col_order.remove('book_id')
header = []
for item in col_order:
    x = []
    x.append(item)
    for element in columns[item]:
        x.append(element['display'])
    header.append(x)

#print header

#use the display name dic to build a header that allows for sorting   
for field, name in header:
    sortflag =''
    if field == order_by:
        sortflag = ' ^'
    js =  "document.form1.order_by.value='%s';" % field
    js += "document.form1.submit();"
    h = '<a onclick="javascript:%s">%s%s</a>' % (js, name, sortflag)
    ordered_header.append(h)
table.addHeader(ordered_header)

# table body
i = 0
activity = 'view'

for rec in results: 
    i += 1
    href = '<a href="detail2.py?book_id=%d&activity=%s">%s'% (rec['book_id'], activity, rec['title'])
    table.addRow([i, href, rec['author'], rec['notes'], rec['date']])

print table.getTable()

### FOOTER

print "</body>"
print "</html>"

