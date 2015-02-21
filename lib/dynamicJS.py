#!usr/bin/env python

import json

from series import Series
from author import Author

class DynamicJS():
     '''responsible for building all dynamic js functions'''

     def autoCSeries(self):
          '''calls the series as dict function, converts the returned dict
          to useable format, reads the series auto complete function,
          populates it with the series dict. Returns working jquery function
          '''
          
          series = Series().getAsAutoCDict()
          ac_series = json.dumps(series)

          return open('/home/jzlink/library/lib/js/series_autocomplete.js')\
              .read() % (ac_series)

 
     def autoCAuthor(self):
          '''calls the author as dict function, converts the returned dict
          to useable format, reads the author  auto complete function,
          populates it with the author dict. Returns working jquery function
          '''

          authors = Author().getAsAutoCDict()
          ac_authors = json.dumps(authors)

          return open('/home/jzlink/library/lib/js/author_autocomplete.js')\
              .read() % (ac_authors)

     def toggle(self, toggler, element):
          ''' accepts an the id of a DOM element that will toggle an other
          DOM element as toggler. element param is the id of the DOM element
          that will be toggled. Returns a working jquery function.'''

          #correctly add quotes before insertion into function
          e = '"'+ element + '"'
          t = '"'+ toggler + '"'
          function = '''
                     $(function(){
                         $(%s).click(function(e){
                                     $(%s).toggle();
                                     e.preventDefault();
                          });
                      }); ''' % (t, e)
          return function

     def datePicker(self): 
          '''returns the js datepicker function initilized for the
          #when_read_datepicker element. NOTE: this is not dynamic, move it
          else where when I actually need it'''

          function ='''
               $(function() {                                                 
                    $( "#when_read_datepicker" ).datepicker();                 
                });'''
          return function


if __name__ =='__main__':
     print autoCseries('SOURCE')
