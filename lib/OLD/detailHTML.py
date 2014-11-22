#!/usr/bin/env python

'''Display Book Record Details'''

from metadata import Metadata
from HTMLutils import HTMLutils
from database import *
from report import Report

class DetailHTML:
    '''Given an actitvity to prefrom on a record (view, edit, add)
       return a list of html building blocks to paint the page''' 

    def __init__(self, book_id, activity):
        self.book_id = book_id
        self.activity = activity
        self.connection = getDictConnection()
        self.conn = getConnection()
        self.htmlUtils = HTMLutils()
        #bring in yaml metadata
        metadata = Metadata()
        self.columns = metadata.loadYaml('columns')
        self.pages = metadata.loadYaml('pages')
        
        if activity == 'edit':
            self.report = Report('edit')
            self.header = 'Edit Record'
            self.page = 'edit'
            self.new_activity = 'update'
            self.button_text = 'Submit'
            self.show_blank = ''
            self.cancel_button_text = 'Cancel'
            self.cancel_button_address = 'detail.py?book_id=%s&activity=view'\
                %book_id

        elif activity == 'view':
            self.report = Report('record')
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
                    $(".author_autocomplete").autocomplete({source: %s});
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

    def build_report(self):

        if self.activity == 'view':
            # make a simple table, not a form
            report = self.report.buildDetail(self.book_id)

        else:
            report = self.report.buildEditBook(self.book_id)

        return report

    def build_input_button(self):
        input_button= '''<div>
         <input type = "hidden" name = "book_id" value = "%s"/>
         <input type = "hidden" name = "activity" value = "%s"/>
         <input type = "button" value = "%s"
              onclick = "javascript: document.form.submit()";/>
         </div>'''% (self.book_id, self.new_activity, self.button_text)
        return input_button
    
    def build_cancel_button(self):
        cancel_button = '''
          <input type = "button" onClick = 
          "location.href='%s'" value = "%s">
           ''' %(self.cancel_button_address, self.cancel_button_text)
        return cancel_button

    def _getAutoCList(self):
        ##TO BE REPLACED BY query.getColumnValues when dict auto complete
        # is enabled

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


