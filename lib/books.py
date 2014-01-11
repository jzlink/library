
from database import getConnection, execute

class Books(object):

    def __init__(self):
        self.connection = getConnection()
        
    def getBooks(self):
        results = execute(self.connection, 
                          'select book_id, title from book')
        #book_id, title =  results[0]
        #return (book_id, title)
        return results


if __name__ == '__main__':
    # test code:
    books = Books()
    results = books.getBooks()
    print "Num of books:", len(results)




