#!/usr/bin/python 

from database import *
from metadata import Metadata
from query import Query
from author import Author

class Record:
    '''Preside over a single record in the database
        including updating it'''

    def __init__(self, book_id, activity):
        '''initialize variables and bring in column metadata'''
        self.book_id = book_id
        self.activity = activity
        self.connection = getDictConnection()
        metadata = Metadata()
        self.columns = metadata.loadYaml('columns')
        self.author = Author()

    def debug(self, record_dict):
        processDict = dict.copy(record_dict)
        return record_dict, self.processRecordDict(processDict)

    def updateRecord (self, record_dict):
        ''' given a dict of column value pairs
        figure out which should be updated
        update tables with new vals if necessary
        return two lists: changes made, values added'''

        original_dict = dict.copy(record_dict)
        book_items = {}
        update_dict = {}
        when_read_items = {}
        series_items = {}
        updated = {}
        added = {}
        removed = {}

        #sort and pre-process dict
        update_dict, author_items = self.processRecordDict(record_dict)

        #send author_items out to be handled
        author_updates = self.updateAuthor(author_items)
        updated.update(author_updates)

        if update_dict:
            for column, value  in update_dict.items():

                record_table = ''

                #figure out which table needs to be updated, amend that dict{}
                record_table = self.columns[column][0]['from']

                if record_table == 'book':
                    book_items.update({column: value})
                if record_table == 'when_read':
                    when_read_items.update({column: value})
                if record_table == 'series':
                    series_items.update({column: value})
        
            if book_items:
                book_updates, book_adds = self.updateBook(book_items)
                updated.update(book_updates)
                added.update(book_adds)

            if series_items:
                series_updates, series_adds = self.updateSeries(series_items)
                updated.update(series_updates)
                added.update(series_adds)

            if when_read_items:
                when_updates, when_adds =  self.updateWhenRead(when_read_items)
                updated.update(when_updates)
                added.update(when_adds)

        return updated, added

    def updateBook(self, book_items):
        updates = {}
        adds = {}
        if self.activity =='add':
            cols = []
            vals = []
            for item in book_items:        
                cols.append(item)
                vals.append(book_items[item])
                adds[item] = book_items[item]
            columns = ', '.join(cols)
            values = ', '.join(vals)
            sql = 'insert into book (%s) values(%s)' %(columns, values)
            
            result = execute(self.connection, sql)

        if self.activity =='update':
            for item in book_items:
                sql = 'update book set %s = %s where book.book_id = %s' \
                    % (item, book_items[item], self.book_id)
                results = execute(self.connection, sql)
                updates[item]= book_items[item]

        return updates, adds

    def updateSeries(self, series_items):
        series_id = 'NULL'
        series = series_items['series']
        updates = {}
        adds ={}

        #if the series recieved isn't blank, check if it is in the DB yet
        #if not add it and append message with that info
        # retrieve the series_id for the requested series
        if series !="''":
            searchSQL = 'select series from series where series like %s'\
                %series
            searchResults = execute(self.connection, searchSQL)

            if not searchResults:
                addSQL = 'insert into series (series) values (%s)' %series
                addResults = execute(self.connection, addSQL)
                adds['series'] = series
            
            IdSQL = 'select series_id from series where series like %s'\
                %series
            IdResults = execute (self.connection, IdSQL)

            series_id = IdResults[0]['series_id']
        
        #set the series_id in the book table to the correct series 
        updateSQL = 'update book set series_id = %s where book_id = %s' \
                % (series_id, self.book_id)
        updateReults = execute(self.connection, updateSQL)
        updates['series'] = series
        return updates, adds

    def updateWhenRead(self, when_read_items):
        updates = {}
        adds = {}
        when = when_read_items['when_read']
        sql = 'insert into when_read (when_read, book_id) values (%s, %s)'\
            %(when, self.book_id)
        results = execute(self.connection, sql)
        adds['when_read'] = when

        return updates, adds

    def updateAuthor(self, author_items):
        remove = []
        add = []
        update = {}
        listofAuthors = []
        authorIdDict = self.author.getAuthorIdDict()
        
        #bring in the data currently in the DB
        authorsOnRecord = self.author.getAuthors(self.book_id, 'concat')
        
        #make a list of names
        for count in range(len(authorsOnRecord)):
            listofAuthors.append(authorsOnRecord[count]['name'])

        #compare the list of names currently in the DB to the author items
        # to see what has to be added or removed
        for item in listofAuthors:
            if item not in author_items:
                remove.append(item)
        
        for item in author_items:
            if item not in listofAuthors:
                add.append(item)

        #add the book_id/author_id pairs to the book_author table
        for item in add:
            author_id = authorIdDict[item]
            sql = '''insert into book_author (author_id, book_id) 
                     values (%s, %s)''' %(author_id, self.book_id)
            results = execute(self.connection, sql)
            update[item] = 'added to record'

        #remove the book_id/author_id pairs from the book_author table
        for item in remove:
            author_id = authorIdDict[item]
            sql = '''delete from book_author 
                     where book_id = %s and author_id = %s
                     ''' %(self.book_id, author_id)
            results = execute(self.connection, sql)
            update[item] = 'removed from record'

        return update

    def processRecordDict(self, record_dict):
        '''given a dict of record items to update prepare them for DB insertion
        by: segregating author items from dict, calling selectDiffColumns,
        prepping the formats of the remaining values for insertion. Returns
        update_dict and author_items'''

        #figure out how many authors this record is expecting
        #move that many items to author_items and delete them from the dict
        author_items = []
        author_num = len(self.author.getAuthors(self.book_id, 'concat'))
        count = 1

        for count in range(author_num):
            count +=1
            author_items.append(record_dict['author_%s' %count])
            del record_dict['author_%s' %count]

        #call selectDiffCols on the remaining dict
        #if that returns any values format them for the DB and return them
        update_dict = self.selectDiffColumns(record_dict)

        if update_dict:
            for column, value in update_dict.items():

                #prep dic vlaues for database update
                if value:
                    update_dict[column]  = "'"+value+"'" 
                elif self.columns[column][0]['type'] == 'string':
                    update_dict[column] = "'" + "'"
                else:
                    value = 'Null'            

        return update_dict, author_items

    def selectDiffColumns(self, recievedData):
        ''' given a dic of data recieve about a record
            compare it to the data in the DB
            remove entries in the recieved dictionary that already exist
            return truncated dict'''
        query = Query()
        where = 'book.book_id =' + str(self.book_id)
        recordData = query.getData('edit', where)
        remove = []
        for col, val in recordData[0].items():
            if val == '':
                recordData[0][col] = None
            else:
                recordData[0][col] = str(val)

        for col in recievedData:
            if recievedData[col] == recordData[0][col]:
                remove.append(col)
        for col in remove:
            del recievedData[col]
                
        return recievedData


edits ={
'author_1': 'Gaiman, Neil', 
'author_2': 'Pratchett, Terry', 
'notes': 'Re-read, I remember it being better', 
'owner_status_id': 
'None', 'published': '1', 
'read_status_id': '1', 
'title': 'Good Omens', 
'type_id': 'None', 
'when_read': '1970-01-01'
}

author_items = ['Gaiman, Neil', 'Barry, Dave'] 

add_dict ={
'last_name': 'Juster', 
'type_id': '6', 
'series': None, 
'date': '1970-01-01', 
'first_name': 'Norton', 
'title': 'The Phantom Tollbooth', 
'owner_status_id': '1', 
'notes': 'Annotated edition. Annotations by Leonard Marcus', 
'series_num': None, 
'published': '1', 
'read_status_id': '1'
}

    
def test():  
   record = Record(335, 'update')
#   add = record.updateRecord(add_dict)
#   update  = record.updateRecord(edits)
   diffCols = record.selectDiffColumns(edits)
#   prep = record.processRecordDict(edits)
#   authors = record.updateAuthor(author_items)


#   print add
#   print update
   print diffCols 
#   print prep
#   print authors

if __name__ == '__main__':
    test()

        
