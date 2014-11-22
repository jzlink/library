#!/usr/bin/python 

from datetime import datetime

from utils import loadYaml
from database import *
from query import Query
from author import Author

class Record:
    '''Preside over a single record in the database
        including updating it'''

    def __init__(self, form_dict):
        '''initialize variables and bring in column metadata'''
        self.book_id = form_dict['book_id']
        self.activity = form_dict['activity']
        self.connection = getDictConnection()
        self.columns = loadYaml('columns')
        self.author = Author()
        self.record_dict = dict.copy(form_dict)
        self.added_new_rec = False

        del self.record_dict['book_id']
        del self.record_dict['activity']        

        if self.activity == 'submit_new':
            start_sql = 'insert into book (title) values ("starter")'
            start = execute (self.connection, start_sql)
            find_sql = "select book_id from book where title like 'starter'"
            find = execute(self.connection, find_sql)
            self.book_id = find[0]['book_id']
            self.activity = 'update'
            self.added_new_rec = True

    def debug(self):
        return self.record_dict, self.processRecordDict()

    def updateRecord (self):
        ''' given a dict of column value pairs
        figure out which should be updated
        update tables with new vals if necessary
        return two lists: changes made, values added'''

        book_items = {}
        update_dict = {}
        when_read_items = {}
        series_items = {}
        updated = {}
        added = {}
        removed = {}

        #sort and pre-process dict
        update_dict, author_items = self.processRecordDict()

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

        #send author_items out to be handled
        author_updates = self.updateAuthor(author_items)
        updated.update(author_updates)

        if self.added_new_rec:
            return self.book_id

        else:
            return updated, added

    def updateBook(self, book_items):
        updates = {}
        adds = {}

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

        if when != '':
            when = (datetime.strptime(when, '%m/%d/%Y')).date()
            when = when.isoformat()
            sql = 'insert into when_read (when_read, book_id) values (%s, %s)'\
                %(when, self.book_id)
            results = execute(self.connection, sql)
            adds['when_read'] = when

        return updates, adds

    def updateAuthor(self, author_items):
        firstLast = author_items.copy()
        fullNames = []
        listofAuthors = []
        authorIdDict = self.author.getAuthorIdDict()
        add = []
        remove = []
        update = {}

        #make a list of full names and a seperate dict for first and last name
        for item in author_items:
            if 'full' in str(item):
                fullNames.append(author_items[item])
                del firstLast[item]

        #If any item in firstLast has a value set newName to true
        newName = False
        for key, value in firstLast.items():
            if value:
                newName = True

        #bring in the data currently in the DB
        authorsOnRecord = self.author.getAuthors(self.book_id, 'concat')

        #make a list of full names in the DB                 
        for count in range(len(authorsOnRecord)):
            listofAuthors.append(authorsOnRecord[count]['name'])

        #compare the list of full names currently in the DB to the
        # full names in author items to see what has to be added or removed
        for item in listofAuthors:
            if item not in fullNames:
                remove.append(item)
        for item in fullNames:
            if item not in listofAuthors:
                add.append(item)
      
        #check if the new first and last name is in the DB yet 
        if newName:
            sql  = '''                                                        
               select author_id from author                                   
               where last_name like '%s' and first_name like '%s'              
               ''' %(author_items['author_last_name'],\
                         author_items['author_first_name'])
            matches = execute(self.connection, sql)

            #if the name is not in the DB add it and refresh the authorIdDict
            if not matches:
                sql = '''
                      insert into author (last_name, first_name)
                      values ('%s', '%s')
                      '''%(author_items['author_last_name'],\
                           author_items['author_first_name'])
                results = execute(self.connection, sql)
                authorIdDict = self.author.getAuthorIdDict()

            #concat the first and last name add it to add list                 
            name = '%s, %s' %(author_items['author_last_name'],\
                                  author_items['author_first_name'])
            add.append(name)

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

    def processRecordDict(self):
        '''given a dict of record items to update prepare them for DB insertion
        by: segregating author items from dict, calling selectDiffColumns,
        prepping the formats of the remaining values for insertion. Returns
        update_dict and author_items'''

        process_dict = dict.copy(self.record_dict)

        author_items = {}
        #find all keys with author in them, add those to author items
        for item in process_dict:
            if 'author' in str(item):
                author_items[item] = process_dict[item]

        #remove all the stuff in author items from record dict
        for item in author_items:
            del process_dict[item]

        #if the acitvity is 'edit'call selectDiffCols on the remaining dict
        #if that returns any values format them for the DB and return them
        #otherwise all values need to be processed
        if self.activity == 'update':
            update_dict = self.selectDiffColumns(process_dict)
        else:
            update_dict = process_dict

        if update_dict:
            for column, value in update_dict.items():
                colType = self.columns[column][0]['type']

                #prep dic vlaues for database update
                if colType == 'string' or colType == 'int':
                    if value:
                        update_dict[column]  = "'"+value+"'"
                    else:
                        update_dict[column] = "'" + "'"
        
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

author_items ={
 'full_names': ['Mcguire, Seanan'], 
 'author_1': 'Mcguire, Seanan'}

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
#   diffCols = record.selectDiffColumns(edits)
#   prep = record.processRecordDict(edits)
   authors = record.updateAuthor(author_items)


#   print add
#   print update
#   print diffCols 
#   print prep
   print authors

if __name__ == '__main__':
    test()

        
