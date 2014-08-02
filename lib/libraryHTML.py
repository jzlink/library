#!/usr/bin/env python

'''Display Book Record Details'''

from query import Query
from utils import date2str
from htmltable import HtmlTable
from loadyaml import LoadYaml
from database import *

class LibraryHTML:
    '''Given an actitvity to prefrom on a record (view, edit, add)
       return a list of html building blocks to paint the page''' 

    def __init__(self, book_id, activity):
        self.book_id = book_id
        self.activity = activity
        self.connection = getDictConnection()
        self.conn = getConnection()
        #bring in yaml metadata
        yaml = LoadYaml()
        self.columns = yaml.loadYaml('columns')
        self.pages = yaml.loadYaml('pages')

        if activity == 'edit':
            self.header = 'Edit Record'
            self.page = 'edit'
            self.new_activity = 'update'
            self.button_text = 'Submit'
            self.show_blank = ''
            self.cancel_button_text = 'Cancel'

        if activity == 'view':
            self.header = 'Book Record' 
            self.page = 'record'
            self.new_activity = 'edit'
            self.button_text = 'Edit'
            self.show_blank = '-'
            self.cancel_button_address = 'main.py'
            self.cancel_button_text = 'Back to Catalog'

        # build the right query for the page and bring in the data 
        self.query = Query()
        where = 'book.book_id =' + str(self.book_id)
        self.recordData = self.query.getData(self.page, where)


    def build_html_header(self):
        html_header= '''
        <html>
        <h3>%s</h3>
        '''%self.header
        return html_header

    def build_form_header(self):
        form_header = '''
        <form method = "POST" action = "detail.py" name = "form">
        '''
        return form_header

    def build_report(self):
        table = HtmlTable(border=1, cellpadding=3)
        table.addHeader(['Field', 'Entry'])

#build list of rows in order of display
        ordered_rows= []
        for item in self.pages[self.page]:
            ordered_rows.append(item)

#build a list of display_names
#build a  list of cols needing drop down menus
        display_names = []
        drop_down = []
        for item in ordered_rows:
            x = []
            x.append(item)
            for element in self.columns[item]:
                if 'foreign_table' in element:
                    drop_down.append(item)
                x.append(element['display'])
            display_names.append(x)

        for col, display in display_names:
            #special handeling to display null values
            for rec in self.recordData:
                if rec[col]:
                    data = rec[col]
                else:
                    data = self.show_blank

            #build simple table for viewing                
            if self.activity == 'view':
                table.addRow([display, data]) 
                
            #build from for editing with drop down menus and text fields
            if self.activity == 'edit':
                if col in drop_down:
                    options = self.getDropDown(col)
                    form_field = '<select name = "%s"> ' %col
                    form_field += options
                    form_field += '</select>'
                else:
                    form_field = '''
                    <input type = "text" name = "%s" value = "%s" size = "100">
                    ''' %(col, data)
                table.addRow([display, form_field])
        #push final product
        report = table.getTable()
        return report

    def build_input_button(self):
        input_button= '''
         <input type = "hidden" name = "book_id" value = "%s"/>
         <input type = "hidden" name = "activity" value = "%s"/>
         <input type = "button" value = "%s"
              onclick = "javascript: document.form.submit()";/>
         '''% (self.book_id, self.new_activity, self.button_text)
        return input_button
    
    def build_cancel_button(self):
#not functioning yet DO NOT INVOKE
        cancel_button = '''
        <form>
         <input type = "hidden" name = "book_id" value = "%s"/>
         <input type = "hidden" name = "activity" value = "view"/>
         <input type = "button" value = "%s"
              onclick = "javascript: document.form.submit()";/>
         </form>
         '''% (self.book_id, self.cancel_button_text)
        return cancel_button

    def build_form_footer(self):
        form_footer = '</form>'
        return form_footer

    def build_html_footer(self):
        html_footer = '</html>'
        return html_footer

    def getDropDown(self, column):
        '''accepts a columns with a foreign table
           returns html for a dropdown menu for that column'''

#retireve columns to select and table to select from
        for item in self.columns[column]:
            select = item['drop_down_select']
            from_table = item['foreign_table']

        sql = 'select %s from %s' %(select, from_table)
        table = execute(self.conn, sql)
       
        options = ''
        
#identify currently set value in record
#if not null make this the default value of the drop down
        for rec in self.recordData:
            current_value = rec[column]

        if current_value:
            current_value_sql = '''
                 select %s from %s where %s = %s
                 ''' %(select, from_table, column, current_value)
            default_value = execute(self.conn, current_value_sql)

            for value in default_value:
                options = ''' 
                <option select = "selected" value = %d> %s</option>
                ''' %(value[0], value[1])
#            table.remove(value)
        else: 
            options ='<option select = "selected" value = "NULL">Pick One</option>'
        
        for item in table:
            option = '''
            <option value = %d> %s</option>
            ''' %(item[0], item[1])
            options += option
          
        return options


def test():  
    libraryHTML = LibraryHTML(335, 'edit')
    html_header = libraryHTML.build_html_header()
    form_header = libraryHTML.build_form_header()
    report = libraryHTML.build_report()
    input_button = libraryHTML.build_input_button()
    cancel_button = libraryHTML.build_cancel_button()
    form_footer = libraryHTML.build_form_footer()
    html_footer = libraryHTML.build_html_footer()
    drop_down = libraryHTML.getDropDown('owner_status_id')

#    print 'hHeader: ' + html_header
    #print 'fHeader: ' + form_header
    print report
   # print 'button: ' + input_button  
    #print ' cancel button: ' + cancel_button
    # print 'fFooter: ' + form_footer
   # print 'hFooter' + html_footer
    print drop_down
  
if __name__ == '__main__':
    test()


