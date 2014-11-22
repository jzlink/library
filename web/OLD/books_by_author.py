#!/usr/bin/env python

from author import Author
#from authors import Authors

# build report body:
authors = Author()
results = authors.booksByAuthor()

# build html table
table = '<table border="1" cellpadding="3" cellspacing="0">\n'
table += ' <tr><th>Author</th><th>Books</th></tr>\n'
for r in results:
    table += ' <tr><td>%s</td><td align="right">%s</td></tr>\n' % r
table += '</table>\n'

# Output HTML
print 'Content-Type: text/html\n'

print "<html>"
print "<h3>Books by Author</h3>"
print table
print "</html>"
