#!/usr/bin/env python

'''Display Book Record Details'''

from query import Query
from utils import date2str
from htmltable import HtmlTable
from metadata import Metadata
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
        metadata = Metadata()
        self.columns = metadata.loadYaml('columns')
        self.pages = metadata.loadYaml('pages')

        if activity == 'edit':
            self.header = 'Edit Record'
            self.page = 'edit'
            self.new_activity = 'update'
            self.button_text = 'Submit'
            self.show_blank = ''
            self.cancel_button_text = 'Cancel'
            self.cancel_button_address = 'detail.py?book_id=%s&activity=view'\
                %book_id

        if activity == 'view':
            self.header = 'Book Record' 
            self.page = 'record'
            self.new_activity = 'edit'
            self.button_text = 'Edit'
            self.show_blank = '-'
            self.cancel_button_address = 'main.py'
            self.cancel_button_text = 'Back to Catalog'

        if activity == 'add':
            self.header = 'Enter New Record' 
            self.page = 'edit'
            self.new_activity = 'submit_new'
            self.button_text = 'Save'
            self.show_blank = ''
            self.cancel_button_address = 'main.py'
            self.cancel_button_text = 'Cancel'
            
        # build the right query for the page and bring in the data 
        if activity != 'add':
            self.query = Query()
            where = 'book.book_id =' + str(self.book_id)
            self.recordData = self.query.getData(self.page, where)
        
    def build_html_header(self):
        html_header= '''
        <html>
        <script src = "jquery_1.11.1.js"></script>
        <link href="css/main.css" rel="stylesheet" type="text/css">
        <script>        
            $( document ).ready(function() {
                $( "a" ).click(function( event ) {
                    alert( "The link will no longer take you to jquery.com" );
                    event.preventDefault();
               });
            });
        </script>
        <h3>%s</h3>
        '''%self.header
        return html_header

    def build_form_header(self):
        form_header = '''
        <form method = "POST" action = "detail.py" name = "form">
        '''
        return form_header

    def build_report(self):
        metadata = Metadata()
        display_data = metadata.interrogateMetadata(self.page, 'display')
        display_names = display_data['col_attributes']
        drop_down_data = metadata.interrogateMetadata(
            self.page, 'foreign_table')
        drop_down = drop_down_data['col_attributes']
                                                   
        table = HtmlTable(border=1, cellpadding=3)
        table.addHeader(['Field', 'Entry'])


        for col, display in display_names:
            #special handeling to display null values
            if self.activity == 'view' or self.activity == 'edit':
                for rec in self.recordData:
                    if rec[col]:
                        data = rec[col]
                    else:
                        data = self.show_blank

            #build simple table for viewing                
            if self.activity == 'view':
                table.addRow([display, data]) 
                
            #build form for editing with drop down menus and text fields
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

            if self.activity == 'add':
                if col in drop_down:
                    options = self.getDropDown(col)
                    form_field = '<select name = "%s"> ' %col
                    form_field += options
                    form_field += '</select>'
                else:
                    form_field = '''
                    <input type = "text" name = "%s" value = "" size = "100">
                    ''' %(col)
                table.addRow([display, form_field])

        #push final product
        report = table.getTable()
        return report

    def build_input_button(self):
        input_button= '''<div>
         <input type = "hidden" name = "book_id" value = "%s"/>
         <input type = "hidden" name = "activity" value = "%s"/>
         <input id = switch type = "button" value = "%s"
              onclick = "javascript: document.form.submit()";/>
         </div>'''% (self.book_id, self.new_activity, self.button_text)
        return input_button
    
    def build_cancel_button(self):
        cancel_button = '''
          <input type = "button" onClick = 
          "location.href='%s'" value = "%s">
           ''' %(self.cancel_button_address, self.cancel_button_text)
        return cancel_button

    def build_form_footer(self):
        form_footer = '</form>'
        return form_footer

    def build_html_footer(self):
        html_footer = '</html>'
        return html_footer

    def getDropDown(self, column):
        '''accepts a column with a foreign table
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
        if self.activity == 'edit':
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
            options ='''
               <option select = "selected" value = "NULL">Pick One</option>'''
        
        for item in table:
            option = '''
            <option value = %d> %s</option>
            ''' %(item[0], item[1])
            options += option
          
        return options


    def build_hidden_section(self):
        hidden =''' 
        <div id = series>
            New Series:
            <input type = 'text' name = 'series'>
            </input>
       </div>
       <button id = hide_series> Show Series </button>
       <script>
           $("#series").hide();
           $("#hide_series").click(function(){
               $("#series").show();
           });
        </script>'''
        return hidden


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
   # print report
   # print 'button: ' + input_button  
    print ' cancel button: ' + cancel_button
    # print 'fFooter: ' + form_footer
   # print 'hFooter' + html_footer
#    print drop_down
  
if __name__ == '__main__':
    test()


