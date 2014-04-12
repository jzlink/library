#!/usr/bin/env python

'''Display Book Record Details'''

# call like this: http://julia-link.com/detail.py?book_id=50

import cgi
import cgitb
cgitb.enable()

from book import Book
from utils import date2str

# get book_id 
form = cgi.FieldStorage()
if 'book_id' not in form:
    book_id = 1
else:
    book_id = form['book_id'].value

if 'activity' not in form:
    activity = 'edit'
else:
    activity = form['activity'].value 

book = Book(book_id, activity)

# build form fields
foo = 'view'

form = '''
<form method = "POST" action = "detail.py/book_id%s&activity=%s">
'''% (book_id, foo)

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
    
#    form +='''<br>
#    %s: <input type = "textfield" name = "entry" value = "%s"><br>
#    '''% (key, value)

    if key == 'title':
        key = 'Title'
        form += '''<br>
        %s: <input type = "textfield" name = "entry" value = "%s"><br>
        '''% (key, value)

    if key == 'last_name':
        key = 'Author Last Name'
        form += '''<br>                                                      
        %s: <input type = "textfield" name = "entry" value = "%s">  
        '''% (key, value)

    if key == 'first_name':
        key = 'First Name'
        form += '''                                                      
        %s: <input type = "textfield" name = "entry" value = "%s"><br>
        '''% (key, value)

    if key == 'notes':
        key = 'Notes'
        form += ''' <br>
        %s: <input type = "textfield" name = "entry" value = "%s"><br>      
        '''% (key, value)

    if key == 'Date Read':
        form += ''' <br>
        %s: <input type = "textfield" name = "entry" value = "%s"><br>      
        '''% (key, value)



form += '''<br>
    <input type = "submit" value = "Update Record">
    </form>\n
    '''

# Output HTML
print 'Content-Type: text/html\n'

print '<html>'
print '<h3>Edit Book Record</h3>'
print form
print '</html>'
