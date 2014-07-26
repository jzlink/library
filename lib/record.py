#!/usr/bin/env python

'''Display Book Record Details'''

from query import Query
from utils import date2str
from htmltable import HtmlTable
from loadyaml import LoadYaml

class Record:
    '''Given an actitvity to prefrom on a record (view, edit, add)
       return a list of html building blocks to paint the page''' 

    def __init__(self, book_id, activity):
        self.book_id = book_id
        self.activity = activity
        
        if activity == 'edit':
            self.header = 'Edit Record'
            self.page = 'edit'
            self.new_activity = 'update'
            self.button_text = 'Submit'
            self.show_blank = ''

        if activity == 'view':
            self.header = 'Book Record' 
            self.page = 'record'
            self.new_activity = 'edit'
            self.button_text = 'Edit'
            self.show_blank = '-'

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

        yaml = LoadYaml()
        columns = yaml.loadYaml('columns')
        pages = yaml.loadYaml('pages')

        query = Query()
        where = 'book.book_id =' + str(self.book_id)

        results = query.getData(self.page, where)

        ordered_rows= []
        for item in pages[self.page]:
            ordered_rows.append(item)

        display_names = []
        drop_down = []
        for item in ordered_rows:
            x = []
            x.append(item)
            for element in columns[item]:
                if 'foreign_table' in element:
                    drop_down.append(item)
                x.append(element['display'])
            display_names.append(x)

        for col, display in display_names:
            for rec in results:
                if rec[col]:
                    data = rec[col]
                else:
                    data = self.show_blank
                
                if self.activity == 'view':
                    table.addRow([display, data]) 
                
                if self.activity == 'edit':
                    if col in drop_down:
                        options = query.getDropDown(col)
                        form_field = '<select name = "%s"> ' %col
                        form_field += options
                        form_field += '</select>'
                    else:
                        form_field = '''
                        <input type = "text" name = "%s" value = "%s"
                        size = "100">''' %(col, data)
                    table.addRow([display, form_field])

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

    def build_form_footer(self):
        form_footer = '</form>'
        return form_footer

    def build_html_footer(self):
        html_footer = '</html>'
        return html_footer

def test():  
    record = Record(1, 'edit')
    html_header = record.build_html_header()
    form_header = record.build_form_header()
    report = record.build_report()
    input_button = record.build_input_button()
    form_footer = record.build_form_footer()
    html_footer = record.build_html_footer()
    #print 'hHeader: ' + html_header
    #print 'fHeader: ' + form_header
    print report
   # print 'button: ' + input_button
   # print 'fFooter: ' + form_footer
   # print 'hFooter' + html_footer
   
if __name__ == '__main__':
    test()


