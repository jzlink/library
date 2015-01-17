#!/usr/bin/env python

'''Display Book Record Details'''

# call like this: http://julia-link.com/detail.py?book_id=50
import cgi
import cgitb
cgitb.enable()

from book import Book
from series import Series
from report import Report
from HTMLutils import HTMLutils
from utils import loadYaml

class Detail():

   def __init__(self):

      self.htmlUtils = HTMLutils()
      self.series = Series()

      self.columns = loadYaml('columns')
      #get form values
      form = cgi.FieldStorage(keep_blank_values = 1)
      self.form_values = {}
      keys =[]
      for k in form.keys():
         key = str(k)
         value = str(form.getvalue(key))
         self.form_values[key] = value

      self.book_id= self.form_values['book_id']
      self.activity= self.form_values['activity']

      self.message = ''
      
      check_again = True

      while check_again:
         if self.activity == 'edit':
            self.report = Report('edit')
            self.table = self.report.buildBookForm(book_id = self.book_id)
            self.header = 'Edit Record'
            self.page = 'edit'
            self.new_activity = 'update'
            self.button_text = 'Submit'
            self.show_blank = None
            self.cancel_button_text = 'Cancel'
            self.cancel_button_address = 'detail.py?book_id=%s&activity=view'\
                %self.book_id
            check_again = False

         elif self.activity == 'view':
            self.report = Report('record')
            self.table = self.report.buildDetail(self.book_id)
            self.header = 'Book Record' 
            self.page = 'record'
            self.new_activity = 'edit'
            self.button_text = 'Edit'
            self.show_blank = '-'
            self.cancel_button_address = 'main.py'
            self.cancel_button_text = 'Back to Catalog'
            check_again = False
            
         elif self.activity == 'add':
            self.report = Report('add')
            self.table = self.report.buildBookForm()
            self.header = 'Enter New Record' 
            self.page = 'edit'
            self.new_activity = 'submit_new'
            self.button_text = 'Save'
            self.show_blank = ''
            self.cancel_button_address = 'main.py'
            self.cancel_button_text = 'Cancel'          
            check_again = False

         elif self.activity == 'update':
            book = Book()
            self.updated = book.updateBook(self.form_values)
         #message = record.debug()
            self.message = 'Yes'
            self.activity = 'view'

         elif self.activity == 'submit_new':
            book = Book()
            self.book_id = book.addBook(self.form_values)
            self.message = 'The following record was added to the libary:'
            self.activity = 'view'

         else:
            raise Exception ("Unrecognized activity: %s" %self.activity)
      

   def buildPage(self):
      page = ''

      form_header = \
          self.htmlUtils.build_form_header('POST', 'detail.py', 'form')
      form_footer = self.htmlUtils.build_form_footer()
      html_footer = self.htmlUtils.build_html_footer()

      if self.message == 'Yes':
         self.message = self.buildMessage(updated = self.updated)

      header = self.buildHeader()
      submit = self.buildInput()
      cancel = self.buildCancel()

      page += 'Content-Type: text/html\n'
      page += header
      page += '<br>'
#      page += self.book_id
      page += self.message
      page += form_header
      page += self.table
      page += '<br>'
      page += submit
      page += cancel
#      page += str(self.form_values)
      page += form_footer
      page += html_footer

      return page

   def buildMessage(self, updated, added= None):
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

      # From a dict {1: 'Trilogy', 3: 'Inheritance', ...}
      # Construct a string of Javascript for Autocomplete()
      #   '[{label: 1, value: "Trilogy"}, {label: 3, value: 'Inheritance'} ...'
      ac_series = '['
      for k,v in Series().getAsDict().items():
         ac_series += '{label: "%s", value: %s}, ' % (v,k)
      ac_series += ']'

      html_header= '''
        <html>
        <link rel="stylesheet" 
           href="//code.jquery.com/ui/1.11.1/themes/smoothness/jquery-ui.css">
           <script src="//code.jquery.com/jquery-1.10.2.js"></script>
           <script src="//code.jquery.com/ui/1.11.1/jquery-ui.js"></script>
        <script>

               $(function() {
                            $("#series_autocomplete").autocomplete({
                               source: %s,
                               focus: function(event, ui) {
                                      event.preventDefault();
                                      $(this).val(ui.item.label);
                                     },
                               select: function(event, ui) {
                                       event.preventDefault();
                                       $(this).val(ui.item.label);
                                       $("#series_ac_key").val(ui.item.value);
                                      }
                              });
                          });

                $(function() {
                    $( "#when_read_datepicker" ).datepicker();
                });

                $(function(){
                    $("#debug").click(function(){
                        $("#debug").toggle();
                     });
                });

        </script>

        <h3>%s</h3>
        '''% (ac_series, self.header)

      return html_header

   def buildInput(self):
      inputValues = ''
      hidden_bookID = self.htmlUtils.getHidden('book_id' , self.book_id)
      hidden_activity = self.htmlUtils.getHidden\
          ('activity', self.new_activity)
      button = self.htmlUtils.getButton\
          (self.button_text,  'javascript:document.form.submit()')

      inputValues = hidden_bookID + hidden_activity + button
      
      return inputValues

   def buildCancel(self):
      onClick = "location.href='%s'" %self.cancel_button_address
      cancel = self.htmlUtils.getButton(self.cancel_button_text, onClick)
      return cancel


if __name__ == '__main__':
    page = Detail()
    print page.buildPage()
