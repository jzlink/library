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

        self.report = report
        self.columns = loadYaml('columns')
        self.pages = loadYaml('pages')

        if report == 'add':
            page = 'edit'
        else:
            page = report

        self.display_names = self.getDisplayNames(page)

    def buildMain(self, where= None, order_by = None):
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
            if rec['date'] == None:
                rec['date'] = '-'
            i += 1
            href = '<a href="detail.py?book_id=%d&activity=%s">%s'\
                % (rec['book_id'], activity, rec['title'])

            mainTable.addRow(\
                [i, href, rec['author'], rec['notes'], rec['date']])

        return mainTable.getTable()

    def buildDetail(self, book_id):
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

    def buildBookForm(self, book_id= None):
        if self.report == 'edit' and book_id != None:
            where = 'book.book_id =' + str(book_id)
            bookData = self.query.getData('edit', where)

        bookTable = HtmlTable(border=1, cellpadding=3)
        bookTable.addHeader(['Field', 'Entry'])

        for column, display in self.display_names:
            form_type = self.columns[column][0]['form_type']

            if self.report == 'edit':
                default = bookData[0][column]
            else:
                default = None

            if column == 'author' or column == 'when_read':
                pass
            
            else:
                #use general methods to build forms
                if form_type == 'text':
                    if default == None:
                        default = ''
                        
                    form_field = self.forms.getTextField(column, default)

                elif form_type == 'drop_down':
                    #pull in the values from the home table to make a 
                    #list of options

                    options = self.query.getColumnValues(column)

                    form_field = \
                        self.forms.getDropDown(column, default, options)

                elif form_type == 'radio_static':
                    if default == None and column == 'published':
                        default = 1

                    options = self.columns[column][0]['radio_options']

                    form_field =\
                        self.forms.getStaticRadio(column, default, options)
 
                elif form_type == 'datepicker':
                    if default == None:
                        default = ''

                    form_field =\
                        self.forms.getJQueryUI(column, default, form_type)

                elif form_type == 'autocomplete':
                    if default == None:
                        default = ''

                    form_field =\
                        self.forms.getAutoComplete(column, default)


                else:
                    form_field = form_type

                bookTable.addRow([display, form_field])
                
        bookT = bookTable.getTable()

        if self.report == 'edit': 
            authorT= self.buildEditAuthor(book_id)
            dateT = self.buildEditDate(book_id)
        else:
            authorT = self.buildAddAuthor()
            dateT = self.buildAddDate()

        subTables = HtmlTable(border=0, cellpadding = 20)
        subTables.addRow([authorT])
        subTables.addRow([dateT])
        subT = subTables.getTable()

        editModules = HtmlTable(border=0, cellpadding=30)
        editModules.addRow([bookT, subT])

        return editModules.getTable()

    def buildEditAuthor(self, book_id):
        author = Author()
        bookAuthor = author.getBookAuthor(book_id)
        editAuthorTable = HtmlTable(border=1, cellpadding=3)
        editAuthorTable.addHeader(['Author', 'Add New Author'])

        for author in bookAuthor:
            catAuthor = '%s %s' %(author['first_name'], author['last_name'])
            remove = 'Remove author %s' %author['author_id']

            editAuthorTable.addRow([catAuthor, remove])

        return editAuthorTable.getTable()


    def buildAddAuthor(self):
        addAuthorTable = HtmlTable(border=0, cellpadding=3)
        autoClist =  self.forms.getJQueryUI('author_id','', 'autocomplete')
        last = self.forms.getTextField('last_name', '')
        first = self.forms.getTextField('first_name', '')
        

        addAuthorTable.addHeader(['Author Exists in Library', 'Add New Author'])
        addAuthorTable.addRow([autoClist, 'First Name:', first])
        addAuthorTable.addRow(['', 'Last Name:', last])
        
        return addAuthorTable.getTable()                     

    def buildEditDate(self, book_id):
        when = WhenRead()
        bookDate = when.getWhenRead(book_id)

        editDateTable = HtmlTable(border=1, cellpadding=3)
        editDateTable.addHeader(['Date', 'Add Addtional Date'])

        for bD in bookDate:
            remove = 'Forget this date'

            editDateTable.addRow([str(bD[0]), remove])

#        return bookDate
        return editDateTable.getTable()        

    def buildAddDate(self):
        datepicker =  self.forms.getJQueryUI('when_read','', 'datepicker')
        addDateTable = HtmlTable(border=1, cellpadding=3)
        
        addDateTable.addRow(['Date', datepicker])

        return addDateTable.getTable()

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
    dateTest = Report('record')
    dateTable = dateTest.buildEditDate(328)
    for d in dateTable:
        print d[0]

#    authorTest = Report('record')
#    authorTable = authorTest.buildEditAuthor(328)
#    print authorTable
#    mainTest = Report('main')
#    mainTable = mainTest.buildMain()
#    mainCols = mainTest.getDisplayNames('main')
#    print mainTest.display_names
#    print mainTest.pages

#    detailTest = Report('record')
#    detailTable = detailTest.buildDetail(335)

#    eBookTest = Report('edit')
#    bookTable = eBookTest.buildEditBook(328)
#    print bookTable

if __name__ == '__main__':
    test()
