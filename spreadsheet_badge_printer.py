#!/usr/bin/python2.4
# -*- coding: latin-1 -*-

import getpass

# has dependencies on pdfgen
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors

import gdata.spreadsheet.service

DOCUMENT_KEY='update to be your key/id from hosted google docs' #comes from the url key=xxxx

"""Prints PDF name badges to fit Avery name badges.
Looks up data from a google spreadsheet (which was using the Form submission feature
to retrieve signups for a conference.) 

Jonathan Andrew Wolter, 2008
"""


class SpreadsheetFetcher:  
  def __init__(self, user, password):
    self.user = user
    self.password = password
  
  def retrieveSpreadsheetsList(self, key=DOCUMENT_KEY):
    client = gdata.spreadsheet.service.SpreadsheetsService()
    client.ClientLogin(self.user, self.password, 'HOSTED') #assumes hosted google docs
    self.spreadsheets_entries_list = client.GetListFeed(key)
    
  def toRegistrantList(self):
    list = []
    for entry in self.spreadsheets_entries_list.entry:
      registration = Registrant(entry.updated.text,
                                  entry.custom['fullname'].text,
                                  entry.custom['ldapusername'].text,
                                  entry.custom['homeoffice'].text,
                                  entry.custom['jobrole'].text,)
      list.append(registration)
    return list

class Registrant:
  def __init__(self, registration_time, full_name, ldap_name, home_office, job_role):
    self.__registration_time = registration_time
    self.full_name = full_name
    self.ldap_name = ldap_name
    self.home_office = home_office
    self.job_role = job_role
    
  def __str__(self):
    return u'%s, a %s from %s' % (self.full_name, self.job_role, self.home_office)
  
class BadgePrinter:
  def __init__(self, registration_list, filename='Badges_rendered.pdf'):
    self.registration_list = registration_list
    self.pdf = Canvas(filename, pagesize = letter)
    
  def drawBadges(self):  
    for six_registrants in self._chunkRegistrantsIntoSixes():
      self._drawOnePage(six_registrants)
    self.pdf.save()
        
  def _drawOnePage(self, registrants):  
    left_column_x = 2.25
    right_column_x = 6.25
    top_y = 9
    middle_y = 6
    bottom_y = 3
    i = 0
    for x in [left_column_x, right_column_x]:
      for y in [top_y, middle_y, bottom_y]:
        if i < len(registrants):
          self._drawOneNameBadge(x, y, registrants[i])
        i += 1      
    self.pdf.showPage()

  def _drawOneNameBadge(self, x, y, registrant):
    self.pdf.setFillColor(colors.black)
#    self.pdf.setFont("Helvetica", 18)
#    self.pdf.drawImage("testing_logo.jpg", (x + 1.1) * inch, (y - .75) * inch)
    self.pdf.setFont("Helvetica", 19)
    self.pdf.drawCentredString(x * inch, y * inch, str(registrant.full_name.encode('latin-1')))
    self.pdf.setFont("Helvetica", 12)
    self.pdf.drawCentredString(x * inch, (y - .25) * inch, str(registrant.home_office))
    self.pdf.setFont("Helvetica", 8)
    self.pdf.drawCentredString(x * inch, (y - .5) * inch, str(registrant.job_role))
    self.pdf.setFont("Helvetica", 6)
    self.pdf.setFillColor(colors.green)
    self.pdf.drawCentredString(x * inch, (y - .7) * inch, 'Test Engineering NYC Summit 2008')

  def _chunkRegistrantsIntoSixes(self):
    chunked = []
    for i in range(0, len(self.registration_list), 6):
      chunked.append(self.registration_list[i:i + 6])
    return chunked
  
def main():        
  user = raw_input("Username [jwolter@example.com]:\n")
  if not user:
    user = 'jwolter@example.com'
  password = getpass.getpass()
        
  # Inject into the NamebadgeMaker all the collaborators, for easy testing
  fetcher = SpreadsheetFetcher(user, password)
  fetcher.retrieveSpreadsheetsList()
  registrats_list = fetcher.toRegistrantList()
  badge_printer = BadgePrinter(registrats_list)
  badge_printer.drawBadges()

if __name__ == '__main__':
  main()