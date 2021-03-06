#!/usr/bin/env python

'''Display Book Record Details'''

# call like this: http://julia-link.com/detail.py?book_id=50

import cgi
import cgitb
cgitb.enable()

from query import Query
from utils import date2str
from htmltable import HtmlTable

# get form values 
form = cgi.FieldStorage()
book_id= form.getvalue('book_id', '1')
activity= form.getvalue('activity', 'edit')

#get editable values from edit form
title=form.getvalue('title')
first_name=form.getvalue('first_name')
last_name=form.getvalue('last_name')
read_status=form.getvalue('status')
series=form.getvalue('series')
notes=form.getvalue('notes')
series_num=form.getvalue('series_num')
owner_status=form.getvalue('owner_status.status')
published=form.getvalue('published')
type=form.getvalue('type')
when_read=form.getvalue('when_read')

formDict = {
        'read_status.status'  : read_status,
        'first_name'          : first_name,
        'last_name'           : last_name,
        'title'               : title,
        'series'              : series,
        'notes'               : notes,
        'series_num'          : series_num, 
        'owner_status.status' : owner_status,
        'published'           : published,
        'type'                : type,
        'when_read.when_read' : when_read
        }
for k, v in formDict.items():
    if v == 'None':
        v = 'NULL'

query = Query()
where = 'book_id =' + book_id
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

#build debug_section
debug_section =  'Book ID = %s' % (book_id)
if title:
    debug_section  = debug_section + ' Title = %s' %title


#build form_header
form_header = '''
    <form method = "POST" action = "detail.py" name = "form">
'''

#bulid report
table = HtmlTable(border=1, cellpadding=3)
table.addHeader(['Field', 'Value'])

if activity == 'edit':
    for key, value in results.data.items():   
        form_field='''
        <input type = 'text' name = '%s' value = '%s' size = '100'> 
        ''' % (key, value)
        table.addRow([key, form_field])

else:
    print results


#report = table.getTable()
        
#buld input_section
eactivity = 'edit'
uactivity = 'update'
vactivity = 'view'

edit_button= '''
       <input type = "hidden" name = "book_id" value = "%s"/>
       <input type = "hidden" name = "activity" value = "%s"/>
       <input type = "button" value = "Edit"
              onclick = "javascript: document.form.submit()";/>
    '''% (book_id, eactivity)

submit_button= '''
     <input type = "hidden" name = "book_id" value = "%s"/>
     <input type = "hidden" name = "activity" value = "%s"/>
     <input type = "button" value = "Confirm Changes"
              onclick = "javascript: document.form.submit()";/>
    '''% (book_id, uactivity)

if activity == 'edit':
    input_section = '<br> %s' %submit_button

else:
    input_section = '<br> %s' %edit_button


form_footer = '</form>'

html_footer = '</html>'

print 'Content-Type: text/html\n'
print results
#print html_header
#print debug_section
#print form_header
#print report
#print input_section
#print form_footer
#if activity == 'update':
#    test = book.editRecord(formDict)
#    activity = 'view'
#    print test
#print html_footer

