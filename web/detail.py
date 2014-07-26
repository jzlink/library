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
from record import Record
from book import Book

# get general form values 
form = cgi.FieldStorage()
book_id= form.getvalue('book_id', '1')
activity= form.getvalue('activity', 'view')

#get form values about a record
title = form.getvalue('title')
last = form.getvalue('last_name')
first = form.getvalue('first_name')
series = form.getvalue('series_name')
series_num = form.getvalue('series_num')
notes = form.getvalue('notes')
date = form.getvalue('date')
o_status = form.getvalue('owner_status')
r_status = form.getvalue('read_status_id')
type_id = form.getvalue('type_id')
pub =  form.getvalue('published')

update_dict = {
'title': title,
'last_name': last,
'first_name': first,
'series_name':series,
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
   book = Book(book_id, activity)
   update = book.updateRecord(update_dict)
   message = "Message: " + update
   activity = 'view'

record = Record(book_id, activity)
html_header = record.build_html_header()
form_header = record.build_form_header()
report = record.build_report()
input_button = record.build_input_button()
form_footer = record.build_form_footer()
html_footer = record.build_html_footer()


print 'Content-Type: text/html\n'
print html_header
print '<br>'
print message
print form_header
print '<br>'
print report
print '</br>'
print input_button
print form_footer
print html_footer

#print "Debug: Activity = " + activity

