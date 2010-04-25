# -*- coding: latin-1 -*-

import unittest

from spreadsheet_badge_printer import BadgePrinter
from spreadsheet_badge_printer import SpreadsheetFetcher
from spreadsheet_badge_printer import Registrant

class BadgePrinterTest(unittest.TestCase):  

  def testRendersUnicodeIntoPdfFromListOfNames(self):
    registrants = [ Registrant('time', u'Jo\xf1\xf1\xf3n Andrew Unicode', 'jwolter', 'US-MTV', 
                           'Green Beret of the Testability Corps'),]
    
    badge_printer = BadgePrinter(registrants, filename='test_rendering_unicode.pdf')
    badge_printer.drawBadges()
    
  def testRenderBadges(self):
    registrants = [ 
                   Registrant('time', 'Jona1than Andrew Wolter', 'jwolter', 'US-MTV', 
                           'Green Beret of the Testability Corps'),
                   Registrant('time', 'Jona2than Andrew Wolter', 'jwolter', 'US-MTV', 
                           'Green Beret of the Testability Corps'),
                   Registrant('time', 'Jona3than Andrew Wolter', 'jwolter', 'US-MTV', 
                           'Green Beret of the Testability Corps'),
                   Registrant('time', 'Jona4than Andrew Wolter', 'jwolter', 'US-MTV', 
                           'Green Beret of the Testability Corps'),
                   Registrant('time', 'Jona5than Andrew Wolter', 'jwolter', 'US-MTV', 
                           'Green Beret of the Testability Corps'),
                   Registrant('time', 'Jona6than Andrew Wolter', 'jwolter', 'US-MTV', 
                           'Green Beret of the Testability Corps'),
                   Registrant('time', 'Jona7than Andrew Wolter', 'jwolter', 'US-MTV', 
                           'Green Beret of the Testability Corps'),
                   Registrant('time', 'Jona8than Andrew Wolter', 'jwolter', 'US-MTV', 
                           'Green Beret of the Testability Corps'),
                   ]        
    printer = BadgePrinter(registrants, filename='test_all_badges_tmp.pdf')
    printer.drawBadges() 
    # manually do a visual inspection
    
  def testChunkListintoSixes(self):
    to_chunk = range(1, 9) # list from 1 to 8, inclusive
    printer = BadgePrinter(to_chunk, 'test_chunk_tmp.pdf',)
    chunked = printer._chunkRegistrantsIntoSixes()
    self.assertEqual(2, len(chunked))
    self.assertEqual(6, len(chunked[0]))
    self.assertEqual(2, len(chunked[1]))
  
    to_chunk = range(1, 7) # list from 1 to 6, inclusive
    printer = BadgePrinter(to_chunk, 'test_chunk_tmp.pdf')
    chunked = printer._chunkRegistrantsIntoSixes()
    self.assertEqual(1, len(chunked))
    self.assertEqual(6, len(chunked[0]))

    to_chunk = []
    printer = BadgePrinter(to_chunk, 'test_chunk_tmp.pdf')
    chunked = printer._chunkRegistrantsIntoSixes()
    self.assertEqual(0, len(chunked))
      
    
    
        
if __name__ == '__main__':
  unittest.main()