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
from author import Author

metadata = Metadata()
pages = metadata.loadYaml('pages')

# get form values 
form = cgi.FieldStorage(keep_blank_values = 1)
form_values = {}
keys =[]
for k in form.keys():
   key = str(k)
   value = str(form.getvalue(key))
   form_values[key] = value

book_id= form_values['book_id']
activity= form_values['activity']

message = ''
if activity == 'update':
   record = Record(form_values)
   message = record.debug()
   updated, added = record.updateRecord()
   message = 'Yes'
   activity = 'view'

if activity == 'submit_new':
   record = Record(form_values)
#   message = record.debug()
   book_id = record.updateRecord()
   message = 'The following record was added to the libary:'
   activity = 'view'
   connection = getDictConnection()

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
#print form_values
print form_footer
print html_footer

