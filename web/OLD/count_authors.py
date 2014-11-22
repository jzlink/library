#!/usr/bin/env python

from author import Author
#from authors import Authors

# build report body:
authors = Author()
count = authors.countAuthors()
body = "<p>There are %s authors in the library.</p>" % count

# Output HTML
print 'Content-Type: text/html\n'

print "<html>"
print "<h3>Count Authors</h3>"
print body
print "</html>"
