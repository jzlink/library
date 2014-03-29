from database import *

class Book(object):
    '''Preside over a single book record in the database'''

    def __init__(self, book_id):
        '''Given a book_id fetch the book data'''
        self.book_id = book_id
        self.connection = getDictConnection()
        self.getData()

    def getData(self):
        sql = '''select title, notes, published, read_status.status, 
owner_status.status, series.series, series.number, type, 
concat(last_name, ', ', first_name) as author 
from book inner join read_status on book.read_status_id= read_status.read_status_id
inner join owner_status on book.owner_status_id=owner_status.owner_status_id
inner join series on book.series_id=series.series_id
inner join type on book.type_id=type.type_id
inner join book_author on book.book_id= book_author.book_id
inner join author on book_author.author_id=author.author_id
where book.book_id=%s''' % self.book_id


        result = execute(self.connection, sql)
        if not result:
            raise Exception('Unable to get book for book_id: %s' %self.book_id)
        self.data = result[0]

    @property
    def owner_status(self):
        '''Return a DICT of the order status for the record
        or empty DICT if there is no order status'''

        if not self.data['owner_status_id']:
            return {}

        sql = 'select * from owner_status where owner_status_id = %s' \
            % self.data['owner_status_id']
        result = execute(self.connection, sql)
        if not result:
            return {}
        return result[0]

def test():
    book = Book(15)
    print book.data

if __name__ == '__main__':
    test()

        
