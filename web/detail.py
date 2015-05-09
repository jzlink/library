#!/usr/bin/env python

'''Display Book Record Details'''

# call like this: http://julia-link.com/detail.py?book_id=50
import cgi
import cgitb
cgitb.enable()
import json

from report import Report
from HTMLutils import HTMLutils
from dynamicJS import DynamicJS
from detailProcessor import DetailProcessor

class Detail():

   def __init__(self):

      self.htmlUtils = HTMLutils()
      self.dynamicJS = DynamicJS()
      self.detailProcessor = DetailProcessor()

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
      
      #if the incoming activity is submit_new or update
      #send form items out to be processed by update processor
      if self.activity == 'submit_new' or self.activity == 'update':
         self.message, self.book_id =\
             self.detailProcessor.processForm(self.form_values)
         self.activity = 'view'

      #set builder variables for each possible activity page
      if self.activity == 'edit':
         self.report = Report('edit')
         self.table = self.report.buildRecordForm(book_id = self.book_id)
         self.header = 'Edit Record'
         self.page = 'edit'
         self.new_activity = 'update'
         self.button_text = 'Submit'
         self.show_blank = None
         self.cancel_button_text = 'Cancel'
         self.cancel_button_address = 'detail.py?book_id=%s&activity=view'\
             %self.book_id

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
         
      elif self.activity == 'add':
         self.report = Report('add')
         self.table = self.report.buildRecordForm()
         self.header = 'Enter New Record' 
         self.page = 'edit'
         self.new_activity = 'submit_new'
         self.button_text = 'Save'
         self.show_blank = ''
         self.cancel_button_address = 'main.py'
         self.cancel_button_text = 'Cancel'          

      else:
         raise Exception ("Unrecognized activity: %s" %self.activity)

   def buildPage(self):
      page = ''

      form_header = \
          self.htmlUtils.build_form_header('POST', 'detail.py', 'form')
      form_footer = self.htmlUtils.build_form_footer()
      html_footer = self.htmlUtils.build_html_footer()

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
#      page += str(self.form_values)
      page += form_footer
      page += html_footer

      return page

   def buildHeader(self):
      '''call in dynamic js functions, add them to the header
      return header'''

      seriesHandler = self.dynamicJS.autoCSeries()
      authorHandler = self.dynamicJS.autoCAuthor()
      dateHandler = self.dynamicJS.datePicker()
      toggleAuthor = self.dynamicJS.toggle('#authorToggle', '#addAuthor')

      html_header= '''
        <html>
        <link rel="stylesheet" 
           href="//code.jquery.com/ui/1.11.1/themes/smoothness/jquery-ui.css">
           <script src="//code.jquery.com/jquery-1.10.2.js"></script>
           <script src="//code.jquery.com/ui/1.11.1/jquery-ui.js"></script>
        <script>
           %s
           %s
           %s
           %s
        </script>

        <h3>%s</h3>
        '''% (seriesHandler, authorHandler, toggleAuthor, dateHandler,\
                 self.header)

      return html_header

   def buildInput(self):
      '''build submit buttons'''

      inputValues = ''
      hidden_bookID = self.htmlUtils.getHidden('book_id' , self.book_id)
      hidden_activity = self.htmlUtils.getHidden\
          ('activity', self.new_activity)
      button = self.htmlUtils.getButton\
          (self.button_text,  'javascript:document.form.submit()')

      inputValues = hidden_bookID + hidden_activity + button
      
      return inputValues

   def buildCancel(self):
      ''' build cancel/go back buttons'''
      onClick = "location.href='%s'" %self.cancel_button_address
      cancel = self.htmlUtils.getButton(self.cancel_button_text, onClick)
      return cancel

if __name__ == '__main__':
    page = Detail()
    print page.buildPage()
