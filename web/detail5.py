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
activity= form.getvalue('activity', 'view')

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
    <form method = "POST" action = "detail.py" name = "form">
'''

#bulid report using metadata. Vary on activity
table = HtmlTable(border=1, cellpadding=3)
table.addHeader(['Field', 'Entry'])

loadyaml = LoadYaml()
columns = loadyaml.loadYaml('columns')
pages = loadyaml.loadYaml('pages')

query = Query()
where = 'book.book_id =' + book_id

if activity == 'view':
    page = 'record'
if activity == 'edit':
    page = 'edit'

results = query.getData(page, where)

ordered_rows= []
for item in pages[page]:
    ordered_rows.append(item)

# making a list of lists holding the col name and display names
# make a list of cols that need drop down menus
display_names = []
drop_down = []
for item in ordered_rows:
    x = []
    x.append(item)
    for element in columns[item]:
        if 'foreign_table' in element:
            drop_down.append(item)
        x.append(element['display'])
    display_names.append(x)

for col, display in display_names:
#    column = columns[col]
    for rec in results:
        if rec[col]:
            data = rec[col]
        else:
            data = "-"
        
        if activity == 'view':
            table.addRow([display, data])

        if activity == 'edit':
            if col in drop_down:
                options = query.getDropDown(col)
                form_field = '<select name = "%s"> ' %col
                form_field += options
                form_field += '</select>'
            else:
                form_field = '''
                <input type = "text" name = "%s" value = "%s" size = "100">
                ''' %(col, data)
            table.addRow([display, form_field])

report = table.getTable()

#input button
if activity == 'view':
    v = 'edit'
    x = 'Edit'

if activity == 'edit':
    v = 'view'
    x = 'Submit'

input_button= '''
       <input type = "hidden" name = "book_id" value = "%s"/>
       <input type = "hidden" name = "activity" value = "%s"/>
       <input type = "button" value = "%s"
              onclick = "javascript: document.form.submit()";/>
    '''% (book_id, v, x)

form_footer = '</form>'
html_footer = '</html>'

print 'Content-Type: text/html\n'
print html_header
print form_header
print report
print '</br>'
print input_button
print form_footer
print html_footer

