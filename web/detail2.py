#!/usr/bin/env python

'''Display Book Record Details'''

# call like this: http://julia-link.com/detail.py?book_id=50

import cgi
import cgitb
cgitb.enable()

from query import Query
from utils import date2str
from htmltable import HtmlTable
from loadyaml import LoadYaml

# get form values 
form = cgi.FieldStorage()
book_id= form.getvalue('book_id', '1')
activity= form.getvalue('activity', 'edit')

query = Query()
where = 'book.book_id =' + book_id
results = query.getData('record', where)

#build html_header
if activity == 'edit':
    header = 'Edit Record'

else:
    header = 'Book Record' 

html_header= '''
   <html>
   <h3>%s</h3>
   '''%header

#build form_header
form_header = '''
    <form method = "POST" action = "detail2.py" name = "form">
</form>
'''

#bulid report
table = HtmlTable(border=1, cellpadding=3)
table.addHeader(['Field', 'Entry'])

loadyaml = LoadYaml()
columns = loadyaml.loadYaml('columns')
pages = loadyaml.loadYaml('pages')

ordered_rows= []
for item in pages['record']:
    ordered_rows.append(item)

display_names = []
for item in ordered_rows:
    x = []
    x.append(item)
    for element in columns[item]:
        x.append(element['display'])
    display_names.append(x)

for col, display in display_names:
    for rec in results:
        if rec[col]:
            data = rec[col]
        else:
            data = "-"
        table.addRow([display, data])

report = table.getTable()

html_footer = '</html>'

print 'Content-Type: text/html\n'
print html_header
print report
print html_footer

