#!/usr/bin/env python
                                                          
import cgi
import cgitb
cgitb.enable()
#enables colored error messages to appear in browser.                          

from search import Search

form = cgi.FieldStorage()

term= form.getvalue('term', 'not entered')

print "Content-type: text/html\n"
print "<html>"

print """
<form method= 'GET' action= " ">
Search Titles For: <input type='text' name = 'term'/>
<input type =  'submit' />
</form>"""

print "<h3> Search term is: %s</h3>" %term
print "</html>"

