#!/usr/bin/python


import cgi
import cgitb
cgitb.enable()

from database import *
from query import Query
from utils import date2str
from htmltable import HtmlTable
from record import Record
from libraryHTML import LibraryHTML
from htmlformtest import TESTLibraryHTML

#libraryHTML = LibraryHTML(3, 'edit')
#form_header = libraryHTML.build_form_header()
#form_footer = libraryHTML.build_form_footer()
#html_footer = libraryHTML.build_html_footer()


test = TESTLibraryHTML(3, 'edit')
report = test.build_report()
textF = test.getTextField('title')
ddF = test.getDropDown('read_status_id')
staticRF = test.getStaticRadio('published')
autoF = test.getAutocomplete('series')
header = test.build_html_header()
input = test.build_input_button()
cancel = test.build_cancel_button()
form_header = test.build_form_header()
form_footer = test.build_form_footer()
html_footer = test.build_html_footer()

print 'Content-Type: text/html\n'
print header
print form_header
print report
print input
print cancel
print form_footer
print html_footer


#print 'Content-Type: text/html\n'
#print html_header
#print '<br>'
#print message
#print form_header
#print '<br>'
#print report
#print series
#print '</br>'
#print input_button
#print cancel_button
#print form_footer
#print html_footer



