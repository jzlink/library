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

# get form values 
form = cgi.FieldStorage()
book_id= form.getvalue('book_id', '1')
activity= form.getvalue('activity', 'view')

record = Record(book_id, activity)
html_header = record.build_html_header()
form_header = record.build_form_header()
report = record.build_report()
input_button = record.build_input_button()
form_footer = record.build_form_footer()
html_footer = record.build_html_footer()


print 'Content-Type: text/html\n'
print html_header
print form_header
print report
print '</br>'
print input_button
print form_footer
print html_footer

print "Debug: Activity = " + activity
