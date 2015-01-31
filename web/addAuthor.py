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

      self.book_id= self.form_values['book_id']
      self.activity= self.form_values['activity']


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
      page += '<br>'
      page += form_header
      page += form
      page += submit
      page += str(self.form_values)
      page += form_footer
      page += html_footer

      return page

   def buildHeader(self):
      authors = self.author.getAsDict()

      # From a dict {1: 'Trilogy', 3: 'Inheritance', ...}
      # Construct a string of Javascript for Autocomplete()
      #   '[{label: 1, value: "Trilogy"}, {label: 3, value: 'Inheritance'} ...'
      ac_series = '['
      for k,v in Series().getAsDict().items():
         ac_series += '{label: "%s", value: %s}, ' % (v,k)
      ac_series += ']'

      ac_authors = json.dumps(authors)
      

      html_header= '''
        <html>
        <link rel="stylesheet" 
           href="//code.jquery.com/ui/1.11.1/themes/smoothness/jquery-ui.css">
           <script src="//code.jquery.com/jquery-1.10.2.js"></script>
           <script src="//code.jquery.com/ui/1.11.1/jquery-ui.js"></script>
        <script>

               $(function() {
                            $("#author_autocomplete").autocomplete({
                               source: %s,
                               focus: function(event, ui) {
                                      event.preventDefault();
                                      $(this).val(ui.item.label);
                                     },
                               change: function(event, ui) {
                                     event.preventDefault();
                                     if (!ui.item){
                                        var fullname = this.value.split(', ');
                                        var first = fullname[1];
                                        var last = fullname[0];
                            var add = confirm('Add '+first +' ' + last + ' to the DB?');
                            if (add){
                                     $("#first_name").val(first);
                                     $("#last_name").val(last);
};
                                     }
                                     else{
                                     event.preventDefault();
                                     $(this).val(ui.item.label);
                                     $("#author_ac_key").val(ui.item.value);
                                     $("#author_id").val(ui.item.value);
                                     $("#first_name").val(ui.item.first_name);
                                     $("#last_name").val(ui.item.last_name);
                                     };
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

        <h3>Adding Authors</h3>
        '''% (ac_authors)

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
