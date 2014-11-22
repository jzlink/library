#!/usr/bin/env python

import yaml

from utils import loadYaml
from query import Query
from htmltable import HtmlTable
from HTMLutils import HTMLutils

class Report():

    def __init__(self, report):
        self.query = Query()
        self.forms = HTMLutils()

        self.columns = loadYaml('columns')
        self.pages = loadYaml('pages')

        self.display_names = self.getDisplayNames(report)

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
            href = '<a href="newdetail.py?book_id=%d&activity=%s">%s'\
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

    def buildEditBook(self, book_id):
        where = 'book.book_id =' + str(book_id)
        bookData = self.query.getData('edit', where)

        editBookTable = HtmlTable(border=1, cellpadding=3)
        editBookTable.addHeader(['Field', 'Entry'])

        for column, display in self.display_names:
            form_type = self.columns[column][0]['form_type']
            default = bookData[0][column]

            if column == 'author':
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
 
                elif form_type == 'autocomplete' or 'datepicker':
                    if default == None:
                        default = ''

                    form_field =\
                        self.forms.getJQueryUI(column, default, form_type)

                else:
                    form_field = form_type

                editBookTable.addRow([display, form_field])

        return editBookTable.getTable()

    def buildEditAuthor(self):
        author = Author()
        names = author.getAuthors(self.book_id, 'concat') 

        form_fields = []
        buttons = []
        count = 0
        for item in names:
            count += 1
            form_field = '''
               <input class = author_autocomplete  name = author_fullname_%s 
                value = '%s'>''' %(count, item['name'])
            form_fields.append(form_field)

        #add hidden section for addtional authors
        buttons.append('''
         <input type = "button" id = "add_author" value = "Add Author">''')

        #add hidden section for brand new authors
        buttons.append('''
         <input type ="button" id = "add_new_author" value = "Add New Author" >
             <div id = "new_author_fields" style = "display:none">
              Last Name:<input type = "text" name = "author_last_name">
              First Name:<input type = "text" name = "author_first_name">
              </div>''')
        author_data = {'form_fields': form_fields, 'buttons':buttons}

        return author_data

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
    mainTest = Report('main')
#    mainTable = mainTest.buildMain()
#    mainCols = mainTest.getDisplayNames('main')
    print mainTest.display_names
    print mainTest.pages

#    detailTest = Report('record')
#    detailTable = detailTest.buildDetail(335)

#    eBookTest = Report('edit')
#    editBookTable = eBookTest.buildEditBook(335)
    
#    print editBookTable

if __name__ == '__main__':
    test()
