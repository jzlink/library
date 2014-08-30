#!/usr/bin/env python

'''Display Book Record Details'''

from query import Query
from utils import date2str
from htmltable import HtmlTable
from metadata import Metadata
from database import *

class TESTLibraryHTML:
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
        <link href="css/main.css" rel="stylesheet" type="text/css">
        <script src = "jquery_1.11.1.js"></script>
        <script>
        $(function(){
        var list = ['abcafvkbev', 'defafsbnvaer', 'ghisvbapqer', 'jklafvbuqeroty', 'mnoagjneuengg'];
        $("#test).autocomplete({source: list});
        });
        </script>
        <h3>%s</h3>
        '''%self.header
        return html_header

    def build_report(self):
        metadata = Metadata()
        display_data = metadata.interrogateMetadata(self.page, 'display')
        display_names = display_data['col_attributes']
        drop_down_data = metadata.interrogateMetadata(
            self.page, 'foreign_table')
        drop_down = drop_down_data['matching_cols']
                                                   
        table = HtmlTable(border=1, cellpadding=3)
        table.addHeader(['Field', 'Entry'])


        for col, display in display_names:

            # make a simple table with special handeling to display null values
            if self.activity == 'view':
                for rec in self.recordData:
                    if rec[col]:
                        data = rec[col]
                    else:
                        data = self.show_blank
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
        return self.recordData


    def getDefault(self, column):
        if self.recordData:
            default = self.recordData[0][column]
        else:
            default = None
        return default


    def getTextField(self, column):
        default = self.getDefault(column)
        if default == None:
            default = self.show_blank

        form_field = '''
         <input type = "text" name = "%s" value = "%s" size = "100">
        '''%(column, default)
        return form_field

    def getDropDown (self, column):
        default = self.getDefault(column)
        colData = self.columns[column][0]

        # pull in the values from the static table
        sql= '''select %s from %s
                ''' %(colData['drop_down_select'], colData['foreign_table'])
        options = execute(self.conn, sql)
        
        form_field = '<select>'

        #if there is no default build a null option Pick One - make it default
        #then build rest of options
        if default == None:
             form_field += '''<option select = "selected" 
                               value = "NULL">Pick One</option>'''
             for o in options:
                form_field += '<option value = %d> %s</option>' %(o[0], o[1])

        # if there is a default loop through data and make it the selected one
        #then build rest of options
        # if default != None and o[0] = default    
        else:
            for o in options:
                if o[0] == default:
                    form_field +=  '''<option select = "selected" 
                               value = %d> %s </option>''' %(o[0], o[1])
                else: 
                    form_field += '''<option value = %d> %s</option>
                                      ''' %(o[0], o[1])
        form_field += '</select>'
        return form_field


    def getStaticRadio(self, column):
        options = self.columns[column][0]['radio_options']
        default = self.getDefault(column)

        if default == 'NULL' and column == 'Published':
            default = 1

        form_field = ''

        # loop through options, identify default, build radio group
        for o in options:
            if o[0] == default:
                form_field += '''<input type = "radio" name = %s value = %d 
                     checked = "true"> %s
                    ''' %(self.columns[column][0]['radio_group'], o[0], o[1])
            else: form_field += '''<input type = "radio" name = %s 
                                 value = %d > %s
                    ''' %(self.columns[column][0]['radio_group'], o[0], o[1])
        
        return form_field

    def getAutocomplete (self, column):
        l = ['abc', 'def', 'ghi', 'jkl', 'mno']
        form_field = '''
               <input id = test>'''
        return form_field


def test():  
    test = LibraryHTML(1, 'edit')
#    report = test.build_report()
    default = test.getDefault('read_status_id')
    textF = test.getTextField('title')
    ddF = test.getDropDown('read_status_id')
    staticRF = test.getStaticRadio('published')
#    print report
#    print default
#    print textF
#    print ddF
    print staticRF
if __name__ == '__main__':
    test()


