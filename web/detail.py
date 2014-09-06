#!/usr/bin/env python

'''Display Book Record Details'''

# call like this: http://julia-link.com/detail.py?book_id=50
import cgi
import cgitb
cgitb.enable()

from database import *
from query import Query
from utils import date2str
from htmltable import HtmlTable
from record import Record
from libraryHTML import LibraryHTML

# get general form values 
form = cgi.FieldStorage()
book_id= form.getvalue('book_id', '1')
activity= form.getvalue('activity', 'view')

#get form values about a record
title = form.getvalue('title')
last = form.getvalue('last_name')
first = form.getvalue('first_name')
series = form.getvalue('series')
series_num = form.getvalue('series_num')
notes = form.getvalue('notes')
date = form.getvalue('when_read')
o_status = form.getvalue('owner_status_id')
r_status = form.getvalue('read_status_id')
type_id = form.getvalue('type_id')
pub =  form.getvalue('published')

record_dict = {
'title': title,
'last_name': last,
'first_name': first,
'series':series,
'series_num': series_num,
'notes': notes,
'date': date,
'owner_status_id': o_status,
'read_status_id': r_status,
'type_id': type_id,
'published': pub
}
message = ''
if activity == 'update':
   record = Record(book_id, activity)
   update = record.updateRecord(record_dict)
   message = "Message: " + update
   activity = 'view'

if activity == 'submit_new':
   record = Record(book_id, 'add')
   add = record.updateRecord(record_dict)
   message = "Message: "
   activity = 'view'
   connection = getDictConnection()
   b_id = execute(connection, 'select max(book_id) from book')
   book_id = b_id[0]['max(book_id)'] 
   

html = LibraryHTML(book_id, activity)
#html_header = html.build_html_header()
report = html.build_report()
html_header = html.build_html_header()
input_button = html.build_input_button()
cancel_button = html.build_cancel_button()
form_header = html.build_form_header()
form_footer = html.build_form_footer()
html_footer = html.build_html_footer()

print 'Content-Type: text/html\n'
print html_header
print '<br>'
print message
print form_header
print report
print '<br>'
print input_button
print cancel_button
print form_footer
print html_footer
