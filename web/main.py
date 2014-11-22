#!/usr/bin/env python

import cgi

#enables color coded error messages
import cgitb
cgitb.enable()

from pprint import pprint

from report import Report
from HTMLutils import HTMLutils

### PROCESS INPUTS
form = cgi.FieldStorage()
term = form.getvalue('term', '')
order_by= form.getvalue('order_by', '')

#instantiate report builder
report = Report('main')

### Build HTML

header_info=  """
<head>
<title> Read A Book! </title>
<link href="css/main.css" rel="stylesheet" type="text/css"\>
</head>"""

##Header
header_text =  "<h1>Julia's Library</h1>"

##Add Book Button
add_book = '''
    <input type = "button" class = 'inputs' onClick = 
      "location.href='detail.py?book_id=0&activity=add'" value = "Add Record"/>
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
    kwd = "'%" + term + "%'"
    where = "title like %s" %kwd

table  = report.buildMain(where = where, order_by = order_by)

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
print table
print footer
