#!/usr/bin/env python

'''Display Book Record Details'''

# call like this: http://julia-link.com/detail.py?book_id=50
import cgi
import cgitb
cgitb.enable()

from record import Record
from report import Report
from HTMLutils import HTMLutils

class Detail():

   def __init__(self, book_id, activity):

      self.htmlUtils = HTMLutils()

      #get form values
      form = cgi.FieldStorage(keep_blank_values = 1)
      self.form_values = {}
      keys =[]
      for k in form.keys():
         key = str(k)
         value = str(form.getvalue(key))
         self.form_values[key] = value

      self.book_id= book_id
      self.activity= activity

      self.message = ''

      if activity == 'edit':
         self.report = Report('edit')
         self.table = self.report.buildEditBook(self.book_id)
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
         self.table = self.report.buildDetail(self.book_id)
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

      if activity == 'update':
         record = Record(form_values)
         #message = record.debug()
         self.updated, self.added = record.updateRecord()
         self.message = 'Yes'
         activity = 'view'

      if activity == 'submit_new':
         record = Record(form_values)
         book_id = record.updateRecord()
         message = 'The following record was added to the libary:'
         activity = 'view'

   def buildPage(self):
      page = ''

      #input_button = self.htmlUtils.build_input_button()
      #cancel_button = self.htmlUtils.build_cancel_button()
      form_header = \
          self.htmlUtils.build_form_header('POST', 'detail.py', 'form')
      form_footer = self.htmlUtils.build_form_footer()
      html_footer = self.htmlUtils.build_html_footer()

      if self.message == 'Yes':
         self.message = self.buildMessage(self.updated, self.added)
         
      header = self.buildHeader()
      submit = self.buildInput()
      cancel = self.buildCancel()

      page += 'Content-Type: text/html\n'
      page += header
      page += '<br>'
      page += self.message
      page += form_header
      page += self.table
      page += '<br>'
      page += submit
      page += cancel
#      page += form_values
      page += form_footer
      page += html_footer

      return page

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


   def buildHeader(self):
      authors = ['list', 'of', 'authors']
      series = ['list', 'of', 'series']
      
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
        '''% (authors, series, self.header)

      return html_header

   def buildInput(self):
      inputValues = ''
      hidden_bookID = self.htmlUtils.getHidden('book_id' , self.book_id)
      hidden_activity = self.htmlUtils.getHidden\
          ('activity', self.new_activity)
      button = self.htmlUtils.getButton\
          (self.button_text, 'javascript: document.form.submit()')

      inputValues = hidden_bookID + hidden_activity + button
      
      return inputValues

   def buildCancel(self):
      onClick = "location.href='%s'" %self.cancel_button_address
      cancel = self.htmlUtils.getButton(self.cancel_button_text, onClick)
      return cancel


def test():
   test = Detail(335, 'view')
#   print test.buildHeader()
   print test.buildPage()

if __name__ == '__main__':
    test()
