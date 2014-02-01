from database import *

class Books:
    '''Preside over Book records in the database'''

    def __init__(self):
        self.connection = getConnection()
        
    def getBooks(self):
        results = execute(self.connection, 
                          'select book_id, title from book')
        #book_id, title =  results[0]
        #return (book_id, title)
        return results
    
    def booksNotesAuthors(self):
        ''' Behavior: returns a list of all books, authors, and notes
        sorted by author'''

        sql= """select title, author, notes                                  
        from book, book_author, author                                    
        where book.book_id=book_author.book_id and                             
        author.author_id=book_author.author_id                                 
        """

        output=execute(self.connection, sql)
        
        return output


if __name__ == '__main__':
    # test code:
    books = Books()
    results = books.getBooks()
    print "Num of books:", len(results)




