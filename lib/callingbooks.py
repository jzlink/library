#!/usr/bin/python

from books import *

test=Books()

result = filter(test.booksNotesAuthors, 'dog')

print result
