#!/usr/bin/env python

import yaml

from utils import loadYaml, date2str
from query import Query
from htmltable import HtmlTable
from HTMLutils import HTMLutils
from author import *
from whenRead import *

class Report():

    def __init__(self, report):
        self.query = Query()

        self.forms = HTMLutils()
        self.author = Author()
        self.when = WhenRead()

        self.report = report
        self.columns = loadYaml('columns')
        self.pages = loadYaml('pages')

        if report == 'add':
            page = 'edit'
        else:
            page = report

        self.display_names = self.getDisplayNames(page)

    def buildMain(self, where= None, order_by = None):
        '''build table seen on main page using all books. Accepts optional
        arguements to filter (search) or sort. Returns table'''

        bookData = self.query.getData('main', where, order_by)

        # start html table
        mainTable = HtmlTable(border=1, cellpadding=3)

        # table header, uses display name and enables sorting
        table_header = ['#']

        for field, name in self.display_names:
            sortflag =''
            if field == order_by:
                sortflag = ' ^'
            js =  "document.form1.order_by.value='%s';" % field
            js += "document.form1.submit();"
            h = '<a onclick="javascript:%s">%s%s</a>' % (js, name, sortflag)
            table_header.append(h)
        mainTable.addHeader(table_header)

        # table body- build a numbered row for each record
        i = 0
        activity = 'view'

        for rec in bookData: 
            i += 1
            href = '<a href="detail.py?book_id=%d&activity=%s">%s'\
                % (rec['book_id'], activity, rec['title'])

            # format dates
            if rec['date']:
                dates = '<br>'.join(['<nobr>%s</nobr>' % d.strip()
                                     for d in rec['date'].split('&')])
            else:
                dates = '-'

            mainTable.addRow(\
                [i,
                 href,
                 rec['author'] or '' ,
                 rec['notes' ]       ,
                 dates])

        return mainTable.getTable()

    def buildDetail(self, book_id):
        '''Static table to view book details'''

        where = 'book.book_id =' + str(book_id)
        bookData = self.query.getData('record', where)

        detailTable = HtmlTable(border=1, cellpadding=3)
        detailTable.addHeader(['Field', 'Entry'])

        for column, display in self.display_names:
            for rec in bookData:
                if rec[column]:
                    data = rec[column]
                else:
                    data = '-'
            detailTable.addRow([display, data])                 

        return detailTable.getTable()

    def buildRecordForm (self, book_id = None):
        '''responisble for building the composite form for book records by
        gathering all data, calling necessary helper methods, and adding all
        sub-forms together. Form has 3 sub-parts:
        (1) the book form which holds all data fields with a 1:1 relationship
        to a book_id 
        (2) the edit author from which itself has 2 sub-parts:
        (2a) the remove author feature (currently inactive) 
        (2b) add author section which defaults to hidden
        (3) the dates read add/remove (currently inactive)
        form is used for adding records and editing records. If a book_id is
        recieved current values for that book_id are pulled from the DB and
        used to pre-populate form fields (used for edit). Otherwise the form
        is built blank, with no default values (used for add).
        Returns composite form as an HTML table
        '''

        #create holder variables
        bookData = None
        authorData = None
        dateData = None

        #bring in data if book_id is present
        if book_id:
            where = 'book.book_id =' + str(book_id)
            bookData = self.query.getData('edit', where)
            authorData = self.author.getBookAuthor(book_id)
            dateData = self.when.getWhenRead(book_id) 
        
        #call helper methods to build all sub-parts
        bookForm = self.buildBookForm(bookData)
        removeAuthor, addAuthor = self.buildEditAuthor(authorData)
        dateForm = self.buildEditDate(dateData)

        #put tables with many:many relationships together in a sub-table table
        subTs = HtmlTable(border=0, cellpadding = 20)
        subTs.addRow([removeAuthor])
        subTs.addRow([addAuthor]) 
        subTs.addRow([dateForm])  
        subTables = subTs.getTable()

        #put all form tables together 
        recordForm  = HtmlTable(border=0, cellpadding=30)
        recordForm. addRow([bookForm, subTables])

        return recordForm.getTable()

    def buildBookForm(self, bookData):
        '''Accepts bookData, which may be blank. 
        Builds book form. If bookData !None pre-populates form with default
        values from bookData.
        returns book form HTML table
        '''
        #initialze book from table
        bookForm = HtmlTable(border=1, cellpadding=3)
        bookForm.addHeader(['Field', 'Entry'])

        #loop through display names (the ordered list of column names)
        #for each: determine the default value and form type
        for column, display in self.display_names:
            form_type = self.columns[column][0]['form_type']

            if self.report == 'edit' and bookData !=None:
                default = bookData[0][column]
            else:
                default = None

            #buld a form field of the correct type
            if form_type == 'text':
                if default == None:
                    default = ''
                form_field = self.forms.getTextField(column, default)

            elif form_type == 'drop_down':
                #pull in the values from the home table to make a 
                #list of options
                options = self.query.getColumnValues(column)
                form_field = self.forms.getDropDown(column, default, options)

            elif form_type == 'radio_static':
                if default == None and column == 'published':
                    default = 1

                #pull in status radio options from metadata
                options = self.columns[column][0]['radio_options']
                form_field =self.forms.getStaticRadio(column, default, options)
 
            elif form_type == 'datepicker':
                if default == None:
                    default = ''

                form_field = self.forms.getJQueryUI(column, default, form_type)

            elif form_type == 'autocomplete':
                if default == None:
                    default = ''

                form_field =self.forms.getAutoComplete(column, default)

            else:
                #debug feature that will make a cell in the table declare
                #what form type it thinks it should be if the form type is not
                #found above
                form_field = form_type

            #add the display name and form field as a new row in the book form
            bookForm.addRow([display, form_field])
                
        return bookForm.getTable()

    def buildEditAuthor(self, authorData):
        '''Accept authorData which may be None
        Build author sub-table. if authorData !None include the list of authors
        and set the add author section to hidden. Else set add author section
        to be visable. Return 2 seperate sections: remove author and add author
        '''

        #initialize Author form
        editAuthorTable = HtmlTable(border=1, cellpadding=3)
        #create button that will toggle open the add author section
        add ='<button type = "button" id="authorToggle"> Add Author </button>'

        #add the header row of the table with the add button
        editAuthorTable.addHeader(['Author', add])

        #build (currently disabled) remove author section
        #section shows list of authors currenlty paired with the book
        #if no authors are pared with the book yet toggle the add author 
        #section open
        if authorData:
            for author in authorData:
                catAuthor = '<nobr>%s %s</nobr>'\
                    %(author['first_name'], author['last_name'])
                remove = 'Remove author %s*' %author['author_id']

                editAuthorTable.addRow([catAuthor, remove])

            #add a note at the bottom of the table re: removing authors
            editAuthorTable.addRow(['',\
                                  '*remove author feature not avalible yet'])

             #initialize hidden add author section
            addAuthor = '<div id = "addAuthor" style = "display: none">'

        else:
            #initialize visable add author section
            addAuthor = '<div id = "addAuthor" style = "display: default">'

        #complete the addAuthor section
        addAuthor += self.buildAddAuthor()
        addAuthor += '</div>'

        return editAuthorTable.getTable(), addAuthor


    def buildAddAuthor(self):
        '''build a table that will be a subtable of the edit author table
        it will be the toggleable section for adding authors to the
        DB and the book record. Only called by buildEditAuthor. Returns table.
        This table will be interacting with the autocomplete js functions.
        '''
        autocomplete = 'Author Name: ' + \
          self.forms.getAutoComplete('author', '',) +\
          '(Last Name, First Name)'
        first_name = 'First Name: ' + \
          self.forms.getTextField ('first_name', '', readonly = True)
        last_name = 'Last Name: '+ \
          self.forms.getTextField ('last_name', '', readonly = True)
        authorForm = autocomplete + '</br>' + first_name + '</br>'+ \
          last_name
        return authorForm

    def buildEditDate(self, dateData):
        '''build table that will be a sub-table of the main edit table to
        hold dates and date addtion/subtraction features. Accepts a book id,
        find associated dates. Returns table'''

        #initilize date table
        editDateTable = HtmlTable(border=1, cellpadding=3)
        editDateTable.addHeader(['Date', 'Add Addtional Date'])

        if dateData:
            for d  in dateData:
                remove = 'Forget this date'
                editDateTable.addRow([str(d[0]), remove])

        return editDateTable.getTable()        

    def getDisplayNames(self, page):
        '''given a page and column attribute 
        return a dictionary of lists:
        ordered_cols: columns in display order
        col_attributes: a list of lists featuring the col and its attribute
                        value
        matching_cols: a list of columns having a feature'''

        ordered_cols = []
        orderedColDisplay = []

        #makes list of columns in display order
        for col in self.pages[page]:
            ordered_cols.append(col)
        if 'book_id' in ordered_cols:
            ordered_cols.remove('book_id')
        
        for col in ordered_cols:
            x = []
        #adds info to correct list if col has attribute
            for element in self.columns[col]:
                    if 'display' in element:
                        x.append(col)
                        x.append(element['display'])                        
                        orderedColDisplay.append(x)

        return orderedColDisplay

def test():
    test = Report('add')
    print test.buildRecordForm()


if __name__ == '__main__':
    test()
