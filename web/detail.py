#!/usr/bin/env python

'''Display Book Record Details'''

# call like this: http://julia-link.com/detail.py?book_id=50

import cgi
import cgitb
cgitb.enable()

from book import Book
from utils import date2str

# get form values 
form = cgi.FieldStorage()
book_id= form.getvalue('book_id', '1')
activity= form.getvalue('activity', 'view')

book = Book(book_id, activity)

# construct page output
table = '<table border="1" cellpadding="3" cellspacing="0">\n'
table += '<tr><th>Column</th><th>Value</th></tr>\n'

if activity == 'edit':
    header= 'Edit Record'
    for key, value in book.data.items():            
        table+= '''
            <form method = "POST" action = "detail.py" name = "edit">
            <tr><td>%s</td><td><input type = 'text' name = '%s' value = '%s' size = '100'</td></tr>\n
    '''% (key, key, value)
    button = '''
     <input type = "hidden" name = "book_id" value = "%s"/>
     <input type = "button" value = "Submit"
          onclick = "javascript: document.edit.submit()";/>
'''% (book_id)

else:
    header= 'Book Record'
    for key, value in book.data.items():

        if value == None:
            value= 'Unknown'

    #Special Handeling for binary field published
        if key =='published':
            key = 'Published'
        if key == 'Published' and value == 1:
            value = 'Yes'
        if key == 'Published' and value == 0:
            value = 'No'
    
    #Special handeling for date output
        if key == 'when_read':
            key= 'Date Read'
            value =date2str(value)
    
        table += ' <tr><td>%s</td><td>%s</td></tr>\n' % (key, value)
    

    eactivity= 'edit'

    button= '''
       <form method = "POST" action = "detail.py" name = "editbutton">
       <input type = "hidden" name = "book_id" value = "%s"/>
       <input type = "hidden" name = "activity" value = "%s"/>
       <input type = "button" value = "Edit"
              onclick = "javascript: document.editbutton.submit()";/>
       </form>
    '''% (book_id, eactivity)

table += '</table>\n'

# Output HTML
print 'Content-Type: text/html\n'

print "<html>"
print "<h3>%s</h3>" %header
print table
print "<br>"
print  button
print "Activity=%s Book ID= %s" % (activity, book_id)
print "</html>"
