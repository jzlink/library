#!/usr/bin/python 

from database import *
from metadata import Metadata
from query import Query

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
        
    
    def updateRecord (self, record_dict):
        ''' given a dict of column value pairs
        figure out which should be updated
        update tables with new vals if necessary
        return two lists: changes made, values added'''

        original_dict = record_dict
        book_items = {}
        author_items = {}
        when_read_items = {}
        series_items = {}
        updated = {}
        added = {}

        #call selectDiff function on recieved dict to determine which fields 
        # should be updated. Update only thoese fields.
        update_dict = self.selectDiffColumns(original_dict)

        if update_dict:
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
        message = ''
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

        
