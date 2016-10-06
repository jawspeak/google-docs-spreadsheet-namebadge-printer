#!/usr/bin/python2.4
# -*- coding: latin-1 -*-

# Takes a CSV import and prints it out as a PDF. Used to take details
# on descriptions of roadmap items that we will work on and print them 
# out to hang in a room and discuss future roadmap stuff (dot voting, etc).

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Frame
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

import csv
import sys
import copy

# how many to print out on the (portrait) oriented page.
# If you want to have multiple columns, use the pdf print
# dialog to have multiple pages per page.
NUM_PER_PAGE = 3

styleSheet = getSampleStyleSheet()

def valFor(record, key):
	return "%s: %s" % (key, record[key]) if record[key] else ''

def drawOnePage(pdf, records):
	# all in inches
	margin = 0.5
	printable_width = 7.5
	each_printable_height = 9.0 / NUM_PER_PAGE

	for i, record in enumerate(records):
		# see reportlab-userguide.pdf page 62.
		story = []
		story.append(Paragraph(str(record['Idea']), styleSheet['Heading1']))
		story.append(Spacer(0,.5*inch))
		story.append(Paragraph(valFor(record, 'Category'), styleSheet['Italic']))
		story.append(Paragraph(valFor(record, 'Bucket'), styleSheet['Italic']))
		story.append(Paragraph(str(record['Internal / External']), styleSheet['Italic']))
		story.append(Paragraph(valFor(record, 'JTBD'), styleSheet['Italic']))

		# reportlab are dimensions from bottom left position.
		#x, y = the bottom left corner of this part of the page to print on.
		x = margin * inch
		y = (i * each_printable_height + margin)*inch
		f = Frame(x, y + margin*i*inch, printable_width*inch, each_printable_height*inch, showBoundary=1)
		f.addFromList(story, pdf)
	pdf.showPage()

def main():
	filename = sys.argv[1]
	pdf = Canvas(filename.replace('.csv', '') + ".pdf", pagesize = letter)

	data = []
	with open(filename, 'rb') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			data.append(row)

	buff = []
	for i, record in enumerate(data):
		if i + 1 == len(data) or len(buff) == NUM_PER_PAGE:
			drawOnePage(pdf, buff)
			buff = []
		else:
			buff.append(record)

	pdf.save()


if __name__ == '__main__':
	if len(sys.argv) != 2:
		print("USAGE: python %s <file.csv>" % sys.argv[0])
		exit(1)
	main()
