#!/usr/bin/env python
                                                          
import cgi
import cgitb
cgitb.enable()
#enables colored error messages to appear in browser.                          

from search import Search
#imports methods from class Search

form = cgi.FieldStorage()

term= form.getvalue('term', 'not entered')
#sets term to 'term'  or else defaults 'term' to not entered 

print "Content-type: text/html\n"
print "<html>"

print """
<form method= 'GET' action= " ">
Search Titles For: <input type='text' name = 'term'/>
<input type =  'submit' />
</form>"""
#generates from that accepts keyword search term

print "<h3> Search Term Is: %s</h3>" %term

titles = Search()
titles.setTerm(term)
result=titles.searchTitle()

print result
print "</html>"

