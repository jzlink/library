#!/usr/bin/python

from books import *

test=Books()

test.booksNotesAuthors()
for row in test.booksNotesAuthors():
    print row
