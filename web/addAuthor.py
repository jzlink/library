#!/usr/bin/env python

'''Display Book Record Details'''

# call like this: http://julia-link.com/detail.py?book_id=50
import cgi
import cgitb
cgitb.enable()
import json

from book import Book
from series import Series
from report import Report
from HTMLutils import HTMLutils
from utils import loadYaml
from author import Author
from jsUtils import *

class addAuthor():

   def __init__(self):

      self.htmlUtils = HTMLutils()
      self.series = Series()
      self.author = Author()

      self.columns = loadYaml('columns')
      #get form values
      form = cgi.FieldStorage(keep_blank_values = 1)

      self.form_values = {}
      keys =[]
      for k in form.keys():
         key = str(k)
         value = str(form.getvalue(key))
         self.form_values[key] = value

      self.book_id= 328
      self.activity= 'view'


   def buildPage(self):
      page = ''

      form_header = \
          self.htmlUtils.build_form_header('POST', 'addAuthor.py', 'form')
      form_footer = self.htmlUtils.build_form_footer()
      html_footer = self.htmlUtils.build_html_footer()

      header = self.buildHeader()
      form = self.buildForm()
      submit = self.buildInput()

      page += 'Content-Type: text/html\n'
      page += header
      page += '<div id = "authorDiv" style = "display: block">'
      page += form_header
      page += form
      page += submit
      page += str(self.form_values)
      page += form_footer
      page += '</div>'
      page += '<button id = "authorToggle"> Add Author </button>'
      page += html_footer

      return page

   def buildHeader(self):
      authors = self.author.getAsDict()
      ac_authors = json.dumps(authors)
      authorHandler = autoCAuthor(ac_authors)

      toggleAuthor = toggle('#authorToggle', '#authorDiv')

      html_header= '''
        <html>
        <link rel="stylesheet" 
           href="//code.jquery.com/ui/1.11.1/themes/smoothness/jquery-ui.css">
       <script src="//code.jquery.com/jquery-1.11.2.min.js"></script>
       <script src="//code.jquery.com/ui/1.11.3/jquery-ui.min.js"></script>

       <script>
         %s
       </script>

        <script>
           %s
        </script>

        <h3>Adding Authors</h3>
        ''' % (authorHandler, toggleAuthor)

      return html_header

   def buildForm(self):
      autocomplete = 'Author Name: ' + \
          self.htmlUtils.getAutoComplete('author', '') + \
          '(Last Name, First Name)'
      first_name = 'First Name: ' + \
          self.htmlUtils.getTextField('first_name', '', readonly = True)
      last_name = 'Last Name: '+ \
          self.htmlUtils.getTextField('last_name', '', readonly = True)
      authorForm = autocomplete + '</br> <p>' + first_name + '</br> <p>'+ \
          last_name
      return authorForm


   def buildInput(self):
      inputValues = ''
      hidden_bookID = self.htmlUtils.getHidden('book_id' , self.book_id)
      hidden_activity = self.htmlUtils.getHidden\
          ('activity', 'add')
      button = self.htmlUtils.getButton\
          ('Submit',  'javascript:document.form.submit()')

      inputValues = hidden_bookID+ hidden_activity + button
      
      return inputValues


if __name__ == '__main__':
    page = addAuthor()
    print page.buildPage()
