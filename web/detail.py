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
from metadata import Metadata
metadata = Metadata()
pages = metadata.loadYaml('pages')

# get general values 
form = cgi.FieldStorage()
book_id= form.getvalue('book_id', '1')
activity= form.getvalue('activity', 'view')

#build dict of values from the book form
form_values = {}
for col in pages['edit']:
   form_values[col] = form.getvalue(col)

#updated = {}
#added = {}

message = ''
if activity == 'update':
   record = Record(book_id, activity)
   updated, added = record.updateRecord(form_values)
   message = 'Yes'
   activity = 'view'

if activity == 'submit_new':
   record = Record(book_id, 'add')
   updated, added = record.updateRecord(form_values)
   activity = 'view'
   connection = getDictConnection()
   b_id = execute(connection, 'select max(book_id) from book')
   book_id = b_id[0]['max(book_id)'] 
   message = 'Yes'
   

html = LibraryHTML(book_id, activity)
html_header = html.build_html_header()
report = html.build_report()
input_button = html.build_input_button()
cancel_button = html.build_cancel_button()
form_header = html.build_form_header()
form_footer = html.build_form_footer()
html_footer = html.build_html_footer()
if message == 'Yes':
   message = html.buildMessage(updated, added)

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

