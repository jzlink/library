#!/usr/bin/python

from classAuthor import *

stats= Author()

stats.countAuthors()
print "There are %s authors in the library." % stats.countAuthors()

stats.booksByAuthor()
for row in stats.booksByAuthor():
    print row
