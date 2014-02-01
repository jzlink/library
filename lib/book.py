from database import *

class Book(object):
    '''Preside over a single book record in the database'''

    def __init__(self, book_id):
        '''Given a book_id fetch the book data'''
        self.book_id = book_id
        self.connection = getDictConnection()
        self.getData()

    def getData(self):
        sql = 'select * from book where book_id = %s' % self.book_id
        result = execute(self.connection, sql)
        if not result:
            raise Exception('Unable to get book for book_id: %s' %self.book_id)
        self.data = result[0]

    # TO DO: - make work
    @property
    def owner_status(self):
        sql = 'select * from owner_status where owner_status_id = %s' \
            % self.data.owner_status_id
        result = execute(self.connection, sql)
        if not result:
            return {}
        return result[0]

def test():
    book = Book(15)
    print book.data

if __name__ == '__main__':
    test()

        
