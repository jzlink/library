#!/usr/bin/env python

'''Display Book Record Details'''

from query import Query
from utils import date2str
from htmltable import HtmlTable
from metadata import Metadata
from database import *
from author import Author

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

        elif activity == 'view':
            self.header = 'Book Record' 
            self.page = 'record'
            self.new_activity = 'edit'
            self.button_text = 'Edit'
            self.show_blank = '-'
            self.cancel_button_address = 'main.py'
            self.cancel_button_text = 'Back to Catalog'

        elif activity == 'add':
            self.header = 'Enter New Record' 
            self.page = 'edit'
            self.new_activity = 'submit_new'
            self.button_text = 'Save'
            self.show_blank = ''
            self.cancel_button_address = 'main.py'
            self.cancel_button_text = 'Cancel'
          
        else:
            raise Exception ("Unrecognized activity: %s" %activity)
  
        # build the right query for the page and bring in the data 
        if activity != 'add':
            self.query = Query()
            where = 'book.book_id =' + str(self.book_id)
            self.recordData = self.query.getData(self.page, where)
        else:
            self.recordData = {}

        #build the dictionary of autocomplete lists by 
        self.autoCompleteList = self._getAutoCList()
        
    def build_html_header(self):
        html_header= '''
        <html>
        <link rel="stylesheet" 
            href="//code.jquery.com/ui/1.11.1/themes/smoothness/jquery-ui.css">
        <script src="//code.jquery.com/jquery-1.10.2.js"></script>
        <script src="//code.jquery.com/ui/1.11.1/jquery-ui.js"></script>
        <script>
                $(function(){
                    $("#author_autocomplete").autocomplete({source: %s});
                    $("#series_autocomplete").autocomplete({source: %s});
                });

                $(function() {
                    $( "#when_read_datepicker" ).datepicker();
                });

                $(function(){
                    $("#add_new_author").click(function(){
                        $("#new_author_fields").toggle();
                     });
                });

        </script>

        <h3>%s</h3>
        '''% (self.autoCompleteList['author'], 
              self.autoCompleteList['series'], 
              self.header)
        return html_header

    def buildMessage(self, updated, added):
        updates = ''
        adds = ''

        if updated:
            updates = 'Updated: <br> '
            for item in updated:
                if item in self.columns:
                    d_name = self.columns[item][0]['display']
                    updates += '%s changed to:  %s <br>'\
                        %(d_name, updated[item])
                else:
                    updates += '%s was %s <br>' %(item, updated[item])

        if added:
            adds = 'Added: <br> '
            for item in added:
                adds += '%s: %s ' %(item, added[item])

        message = 'For this record the following fields were <br> %s %s'\
            %(updates, adds)

        if not added and not updated:
            message = 'Message: No fields changed, no updates made'
        
        return message

    def build_form_header(self):
        form_header = '''
        <form method = "POST" action = "detail.py" name = "form">
        '''
        return form_header

    def build_report(self):
        metadata = Metadata()
        display_data = metadata.interrogateMetadata(self.page, 'display')
        display_names = display_data['col_attributes']
        table = HtmlTable(border=1, cellpadding=3)
        table.addHeader(['Field', 'Entry'])


        for column, display in display_names:
            if self.activity == 'view':
            # make a simple table, not a form
                for rec in self.recordData:
                    if rec[column]:
                        data = rec[column]
                    else:
                        data = self.show_blank
                table.addRow([display, data])                 

            else:
                if column == 'author':
                    #use special method to build author part
                    form_field = self.getAuthorSection()

                else:
                    #use general methods to build forms
                    form_type = self.columns[column][0]['form_type']
                    type_method_func = {'text'        : self.getTextField,
                                        'drop_down'   : self.getDropDown,
                                        'radio_static': self.getStaticRadio,
                                        'autocomplete': self.getJQueryUI,
                                        'datepicker'  : self.getJQueryUI
                                        }
                    form_field = type_method_func[form_type](column)

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

    def getAuthorSection(self):
        author = Author()
        names = author.getAuthors(self.book_id, 'concat') 

        form_field= ''
        count = 0
        for item in names:
            count += 1
            form_field += '''
               <input id = author_autocomplete  name = author_%s value = '%s'>
                  ''' %(count, item['name'])
            
        #add hidden section for addtional authors
        form_field +='''
         <input type = "button" id = "add_author" value = "Add Author">'''

        #add hidden section for brand new authors
        form_field +='''
         <input type ="button" id = "add_new_author" value = "Add New Author" >
             <div id = "new_author_fields" style = "display:none">
              Last Name:<input type = "text" name = "last_name">
              First Name:<input type = "text" name = "first_name">
              </div>'''

        return form_field

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
        
        form_field = '<select required name = %s>' %column

        #if there is no default build a null option - make it default
        if default == None:
             form_field += '''<option selected = "selected" 
                               value = None>(None)</option>'''
        #check if each option should be set to default else build as normal
        for o in options:
            if o[0] == default:
                form_field +=  '''<option selected = "selected" 
                               value = %d> %s </option>''' %(o[0], o[1])
            else: 
                form_field += '''<option value = %d> %s</option>
                                      ''' %(o[0], o[1])
        form_field += '</select>'
        return form_field

    def getStaticRadio(self, column):
        options = self.columns[column][0]['radio_options']
        default = self.getDefault(column)

        if default == None and column == 'published':
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

    def getJQueryUI (self, column):
        form_type = self.columns[column][0]['form_type']
        default = self.getDefault(column)
        if default == None:
            default = self.show_blank
 
        form_field = '''
                   <input id = %s_%s  name = %s value = '%s'>
                  ''' %(column, form_type, column, default)
        return form_field

    def _getAutoCList(self):
        '''Behavior: populate acList{}
           with dic of lists to use by autocomplete fields'''
        aclist = {}

        for column in self.columns:
            resultsList = []

            if 'form_type' in self.columns[column][0] and \
                    self.columns[column][0]['form_type'] == 'autocomplete':

                sql = '''select %s from %s group by %s_id
                ''' % (self.columns[column][0]['select'],
                       self.columns[column][0]['from'], column)
                results = execute(self.conn, sql)
                for item in results:
                    resultsList.append(item[0])
                    aclist[column] = resultsList

        return aclist


def test():  
    u = {'series': 'Cat Power', 'series_num': 1}
    a = {'series': 'Cat Power'}
    uu = {}
    aa = {}

    test = LibraryHTML(328, 'edit')
#    report = test.build_report()
#    default = test.getDefault('author')
#    textF = test.getTextField('title')
#    ddF = test.getDropDown('owner_status_id')
#    staticRF = test.getStaticRadio('published')
#    autoCF = test.getJQueryUI('when_read', 'datepicker')
#    autolist = test._getAutoCList()
#    message = test.buildMessage(u,a)
    author = test.getAuthorSection()

#    print report
#    print default
#    print textF
#    print ddF
#    print staticRF
#    print autoCF
#    print autolist
#    print message
#    print test.autoCompleteList
    print author

if __name__ == '__main__':
    test()


