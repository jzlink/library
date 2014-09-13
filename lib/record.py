#!/usr/bin/python 

from database import *
from metadata import Metadata
from query import Query

class Record:
    '''Preside over a single book record in the database'''

    def __init__(self, book_id, activity):
        '''Given a book_id fetch the book data'''
        self.book_id = book_id
        self.activity = activity
        self.connection = getDictConnection()
        metadata = Metadata()
        self.columns = metadata.loadYaml('columns')
        
    
    def updateRecord (self, record_dict):
        original_dict = record_dict
        book_items = {}
        author_items = {}
        when_read_items = {}
        series_items = {}
        update_dict = self.selectDiffColumns(original_dict)

        if update_dict:
#            message = 'For %s: ' %record_dict['title']
            message = ''
            for column, value  in update_dict.items():
                record_table = ''
            
            #prep dic vlaues for database update
                if value:
                    value  = "'"+value+"'" 
                elif self.columns[column][0]['type'] == 'string':
                    value = "'" + "'"
                else:
                    value = 'Null'

            #figure out which table needs to be updated, amend that dict{}
                record_table = self.columns[column][0]['from']

                if record_table == 'book':
                    book_items.update({column: value})
                if record_table == 'author':
                    author_items.update({column: value})
                if record_table == 'when_read':
                    when_read_items.update({column: value})
                if record_table == 'series':
                    series_items.update({column: value})
        
            if book_items:
                message += self.updateBook(book_items)

            if series_items:
                message += self.updateSeries(series_items)

            if when_read_items:
                message += self.updateWhenRead(when_read_items)

        else:
            message = 'Nothing to Update'

        return message


    def updateBook(self, book_items):
        message = ''
        updates = []
        if self.activity =='add':
            cols = []
            vals = []
            for item in book_items:        
                cols.append(item)
                vals.append(book_items[item])
            columns = ', '.join(cols)
            values = ', '.join(vals)
            sql = 'insert into book (%s) values(%s)' %(columns, values)
            
            result = execute(self.connection, sql)
            message = "book sucessfully added"

        if self.activity =='update':
            for item in book_items:
                sql = 'update book set %s = %s where book.book_id = %s' \
                    % (item, book_items[item], self.book_id)
                results = execute(self.connection, sql)
                updates.append(item)
            message = ', '.join(updates) + " sucessfully updated."
        return message

    def updateSeries(self, series_items):
        series_id = 'NULL'
        series = series_items['series']
        message = ' Series was updated to %s.' %(series)

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
                message += ' Series %s added to database.' %series
            
            IdSQL = 'select series_id from series where series like %s'\
                %series
            IdResults = execute (self.connection, IdSQL)

            series_id = IdResults[0]['series_id']
        
        #set the series_id in the book table to the correct series 
        updateSQL = 'update book set series_id = %s where book_id = %s' \
                % (series_id, self.book_id)
        updateReults = execute(self.connection, updateSQL)

        return message

    def updateWhenRead(self, when_read_items):
        when = when_read_items['when_read']
        sql = 'insert into when_read (when_read, book_id) values (%s, %s)'\
            %(when, self.book_id)
        results = execute(self.connection, sql)
        
        return 'Date read %s added.' %( when)


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
            recordData[0][col] = str(val)

        for col in recievedData:
            if recievedData[col] == recordData[0][col]:
                remove.append(col)
        for col in remove:
            del recievedData[col]
                
        return recievedData



edits ={
'author': 'Mcguire, Seanan', 
'series': 'October Daye', 
'notes': 'October Daye bk. 2', 
'title': 'A Local Habitation', 
'series_num': '2', 
'owner_status_id': '1', 
'type_id': '5', 
'read_status_id': '1', 
'when_read': '2010-06-05', 
'published': '1'
}

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
   update  = record.updateRecord(edits)
#   diffCols = record.selectDiffColumns(edits)

#   print add
   print update
#   print diffCols 

#   print edits['title']

if __name__ == '__main__':
    test()

        
