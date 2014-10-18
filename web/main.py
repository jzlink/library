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

##Retrieve metaData
metadata = Metadata()
#instantiate query
query= Query()


### Build HTML

header_info=  """
<head>
<title> Read A Book! </title>
<link href="css/main.css" rel="stylesheet" type="text/css">
</head>"""

##Header
header_text =  "<h1>Julia's Library</h1>"

##Add Book Button
add_book = '''
    <input type = "button" class = 'inputs' onClick = 
      "location.href='detail.py?book_id=0&activity=add'" value = "Add Record">
'''

##Search Section
search =  """
<form method="POST" action="main.py" name="form1" class = 'inputs'> 
Search Titles For: 
<input type='textfield' name ='term' value='%s'/>
<input type='submit' value='submit'/>
<input type='button' value='clear' 
       onclick="javascript:document.form1.term.value=''; 
                document.form1.submit();"/>
<input type='hidden' name='order_by' value='%s'/>
</form>""" % (term, order_by)

### TABLE OF BOOKS
#retrieve system data
where = ''
if term:
    print 'Search term is %s' %term
    kwd = "'%" + term + "%'"
    where = "title like %s" %kwd

results = query.getData('main', where, order_by)
data = metadata.interrogateMetadata('main', 'display')
display_names = data['col_attributes'] 

# build html table
table = HtmlTable(border=1, cellpadding=3)

# table header
table_header = ['#']

#use the display_name list to build a header that enables sorting   
for field, name in display_names:
    sortflag =''
    if field == order_by:
        sortflag = ' ^'
    js =  "document.form1.order_by.value='%s';" % field
    js += "document.form1.submit();"
    h = '<a onclick="javascript:%s">%s%s</a>' % (js, name, sortflag)
    table_header.append(h)
table.addHeader(table_header)

# table body
i = 0
activity = 'view'

for rec in results: 
    i += 1
    href = '<a href="detail.py?book_id=%d&activity=%s">%s'% (rec['book_id'], activity, rec['title'])
    table.addRow([i, href, rec['author'], rec['notes'], rec['date']])

### FOOTER
footer = '</body> </html>'

#paint HTML on page
print 'Content-Type: text/html\n'
print '<html>'
print header_info
print '<body>'
print "<header role = 'banner' div id = 'header-fixed'>"
print header_text
print add_book
print search
print "</header>"
print "</div>"
print table.getTable()
print footer
