#!/usr/bin/env python

'''Display Book Record Details'''

# call like this: http://julia-link.com/detail.py?book_id=50

import cgi
import cgitb
cgitb.enable()

from book import Book
from utils import date2str
from htmltable import HtmlTable

# get form values 
form = cgi.FieldStorage()
book_id= form.getvalue('book_id', '1')
activity= form.getvalue('activity', 'view')

#get editable values from edit form
title=form.getvalue('title')
first_name=form.getvalue('first_name')
last_name=form.getvalue('last_name')
status=form.getvalue('status')
series=form.getvalue('series')
notes=form.getvalue('notes')
series_num=form.getvalue('series_num')
owner_status=form.getvalue('owner_status.status')
publised=form.getvalue('published')
type=form.getvalue('type')
when_read=form.getvalue('when_read')

book = Book(book_id, activity)

#build html_header
if activity == 'edit':
    header = 'Edit Record'
elif activity == 'update':
    header = 'Preview Changes to Record'
else:
    header = 'Book Record' 

html_header= '''
   <html>
   <h3>%s</h3>
   '''%header

#build debug_section
debug_section =  'Activity = %s Book ID = %s' % (activity, book_id)
if title:
    debug_section  = 'Title = %s' %title

#build form_header
form_header = '''
    <form method = "POST" action = "detail.py" name = "form">
'''


#bulid report
table = HtmlTable(border=1, cellpadding=3)
table.addHeader(['Field', 'Value'])

if activity == 'edit':
    for key, value in book.data.items():   
        form_field='''
        <input type = 'text' name = '%s' value = '%s' size = '100'> 
    ''' % (key, value)
        table.addRow([key, form_field])
       
else:
    for key, value in book.data.items():   
        string_value = '%s' %value
        table.addRow([key, string_value]) 

report = table.getTable()
        
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

preview_button = '''
     <input type = "hidden" name = "book_id" value = "%s"/>
     <input type = "hidden" name = "activity" value = "%s"/>
     <input type = "button" value = "Preview"
          onclick = "javascript: document.form.submit()";/>
     '''% (book_id, uactivity)

submit_button= '''
     <input type = "hidden" name = "book_id" value = "%s"/>
     <input type = "hidden" name = "activity" value = "%s"/>
     <input type = "button" value = "Submit"
              onclick = "javascript: document.form.submit()";/>
    '''% (book_id, vactivity)

if activity == 'edit':
    input_section = '<br> %s' %preview_button

if activity == 'view':
    input_section = '<br> %s' %edit_button

if activity == 'update':
    input_section = '<br> %s' %submit_button


form_footer = '</form>'

html_footer = '</html>'

print 'Content-Type: text/html\n'
print html_header
print debug_section
print form_header
print table.getTable()
print input_section
print form_footer
print html_footer

