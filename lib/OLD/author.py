#!/usr/bin/python

from  database import *
from metadata import Metadata
class Author:
    '''presides over author data'''

    def __init__(self):
        self.connection = getDictConnection()
        metadata = Metadata()
        self.columns = metadata.loadYaml('columns')
        self.authorData = self.columns['author'][0] 

    def getAuthors(self, book_id, output):
        ''' given a book_id return the author(s) of that book as a dictionary 
        in one of two outputs: first/last seperated or first/last concatenated
        seperate: {'last_name': 'Smith', 'first_name': 'John'}
        concat: {'name': 'Smith, John'}'''

        if output == 'seperate':
            sql = '''select last_name, first_name, a.author_id
                 from author a
                 join book_author ba on a.author_id = ba.author_id
                 where ba.book_id = %s''' %(book_id)

        if output == 'concat':
            sql = '''select %s as name, a.author_id 
                     from author a
                     join book_author ba on a.author_id = ba.author_id
                     where ba.book_id = %s
                     group by author_id
                     '''%(self.authorData['select'], book_id)

        results = execute(self.connection, sql)
        
        return results

    def getAuthorIdDict(self):
        '''Behavior: return a dicionary of concatenated 
        last, first names: author_id's. It will be used to find the author id 
        given a concatenated name such as the one used to populate the 
        autocomplete list. The same concatenating phrase, pulled from the 
        metadata, is used in both goups to ensure matching'''

        name_dict = {}
        sql = 'select %s as name, author_id from author group by author_id' \
            %(self.authorData['select'])
        results = execute(self.connection, sql)

        for author in results:
            name_dict[author['name']] = author['author_id']
        
        return name_dict

def test():  
    test = Author()
    authors = test.getAuthors(328, 'concat')
    num= len(authors)
    author_dict = test.getAuthorIdDict()

#    print authors
    print author_dict
if __name__ == '__main__':
    test()

