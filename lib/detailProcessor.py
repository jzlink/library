#!/usr/bin/env python

from book import Book
from series import Series
from author import Author
from whenRead import WhenRead
from utils import loadYaml

class DetailProcessor():

   def __init__(self):

      self.series = Series()
      self.author = Author()
      self.book = Book()
      self.whenRead = WhenRead()

      #establish list of fields the book method is purely responsible for
      # updating
      self.bookOnlyFields = ['book_id', 'title', 'notes', 'published',
                             'owner_status_id', 'read_status_id', 'type_id', 
                             'series_num']

   def processForm(self, formDict):

      message = 'Record Updated'
      book_id = formDict['book_id']
      #if the record is new first call the add new book method, reciecve a new
      # book_id, append it to the dictionary
      # the send the dictionary to the update methods
      if formDict['activity'] == 'submit_new':
         book_id = self.book.addBook()
         formDict['book_id'] = book_id
         message = 'Record Added'

      bookDict = {}
      #create a special dictionary of fields the book method is responsible for
      # updating itself.
      for field in self.bookOnlyFields:
         bookDict[field] = formDict[field]

      #run the seriesUpdate method which will add a series to the DB if
      # necessary. append the new series id to the  bookDict
      seriesUpdate = self.series.updateSeries(formDict)
      bookDict['series_id'] = seriesUpdate

      bookUpdate = self.book.updateBook(bookDict)
      authorUpdate = self.author.updateAuthor(formDict)

      if formDict['when_read'] != '':
         dateUpdate = self.whenRead.updateWhenRead(formDict)

      #message =  self.buildMessasge() # insert all update return values
      return message, book_id

   def buildMessage(self, updated, added= None):
      '''accepts dict of fields updated and their new values
      returns properly formatted string for message display'''

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

def test():
    test = DetailProcessor()
    testDict = {'series_id': '', 'first_name': 'Terry',
                'last_name': 'Pratchett', 'title': 'Jigo',
                'series': 'Discworld', 'notes': '', 'author': '',
                'series_num': '21', 'book_id': '', 'owner_status_id': '2', 
                'type_id': '1', 'author_id': '', 'activity': 'submit_new',
                'read_status_id': '1', 'published': '1'}

    update = test.processForm(testDict)
    print update

if __name__ == '__main__':
    test()
