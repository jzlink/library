#!/usr/bin/env python

import unittest

from author import Author

#fixtures
BOOK_AUTHORS_ID = 328

BOOK_AUTHORS = ({'first_name': 'Neil', 'last_name': 'Gaiman', 'author_id': 59L}, {'first_name': 'Terry', 'last_name': 'Pratchett', 'author_id': 147L})

class TestAuthor(unittest.TestCase):
    
    def setUp(self):
        self.author = Author()        

    def test_getBookAuthor(self):
        bookAuthors = self.author.getBookAuthor(BOOK_AUTHORS_ID)
        self.assertEqual(bookAuthors, BOOK_AUTHORS)

    def testA(self):
        self.assertEqual(1,1)

    def testB(self):
        self.assertNotEqual(1,2)





if __name__ == '__main__':
    unittest.main()





