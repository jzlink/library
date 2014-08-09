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

print "<header role = 'banner'>"
##Header
print "<h3>Julia's Library</h3>"

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

print "<div id = 'header-fixed'>"
print "</header>"
print "</div>"

### TABLE OF BOOKS

query= Query()
results = query.getData('main', where, order_by)

loadyaml = LoadYaml()
columns = loadyaml.loadYaml('columns')
pages = loadyaml.loadYaml('pages')

# build html table
table = HtmlTable(border=1, cellpadding=3)

# table header
#use ordered list from pages.yml to make an ordered list of lists in this form:
#['column', 'display name']. Use this list to develop the header.

ordered_cols= []
for item in pages['main']:
    ordered_cols.append(item)
ordered_cols.remove('book_id') #we don't want book_id to be a column heading

display_names = []
for item in ordered_cols:
    x = []
    x.append(item)
    for element in columns[item]:
        x.append(element['display'])
    display_names.append(x)

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

