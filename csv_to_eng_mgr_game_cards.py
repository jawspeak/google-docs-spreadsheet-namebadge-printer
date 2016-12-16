#!/usr/bin/python2.4
# -*- coding: latin-1 -*-

# Takes a CSV import and prints it out as a PDF. Used to make the EM game
# class cards for play testing in my EM class.

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
heading = copy.deepcopy(styleSheet['Heading1'])
heading.fontSize += 2

italic = copy.deepcopy(styleSheet['Italic'])
italic.fontSize += 2

smallItalic = copy.deepcopy(styleSheet['Italic'])

# colorsForCategories = [
# 	colors.darkseagreen, 
# 	colors.darkslateblue,
# 	colors.darkblue,
# 	colors.darkcyan,
# 	colors.darkolivegreen,
# 	colors.indigo,
# 	colors.brown,
# 	colors.palegoldenrod,
# 	colors.cornflower,
# 	colors.orchid]

def printableColors():
	allColors = colors.getAllNamedColors()
	colorsForCategories = colors.getAllNamedColors().values()
	for k in allColors.keys():
		for unwantedName in ['white', 'yellow', 'CMYK', 'black', 'transparent']:
			if k.find(unwantedName) > -1: 
				print "removing %s" % k
				if allColors[k] in colorsForCategories:
					colorsForCategories.remove(allColors[k])
	return colorsForCategories

colorsForCategories = printableColors()
categoryColor = {}

def valFor(record, key, printKey=False):
	if printKey:
		return "%s: %s" % (key, record[key]) if record[key] else ''
	else:
		return "%s" % record[key]

def colorizeCategory(category):
	style = copy.deepcopy(heading)
	if len(categoryColor) + 1 > len(colorsForCategories):
		print "Warning: more categorized colorized than colors defined, will repeat colors."
	if category not in categoryColor:
		categoryColor[category] = colorsForCategories[len(categoryColor) % len(colorsForCategories)]
	style.textColor = categoryColor[category]
	return style

def drawOnePage(pdf, records):
	# all in inches
	margin = 0.25
	printable_width = 7.5
	each_printable_height = 8.0 / NUM_PER_PAGE


	for i, record in enumerate(records):
		# see reportlab-userguide.pdf page 62.
		story = []
		# story.append(Paragraph(str(record['Idea']), heading))
		# story.append(Spacer(0,.5*inch))

		story.append(Spacer(0,.05*inch))
		style = colorizeCategory(record['Type'])
		story.append(Paragraph(str(record['Type']), style))
		story.append(Spacer(0,.1*inch))

		story.append(Paragraph(valFor(record, 'Text'), heading))
		
		#debugging colors i don't want and need to exclude
		# story.append(Paragraph(str(style.textColor), italic))
		
		# story.append(Paragraph(valFor(record, 'Bucket'), italic))
		# story.append(Paragraph(str(record['Internal / External']), italic))
		# story.append(Paragraph(valFor(record, 'JTBD'), italic))
		# story.append(Paragraph(valFor(record, 'Total Votes'), smallItalic))

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
		if (i + 1 == len(data) and len(buff) > 0) or (len(buff) == NUM_PER_PAGE):
			drawOnePage(pdf, buff)
			print "printing, i= %s, buff len %s" % (i, len(buff)) 
			buff = []
		else:
			if len(record['Type'].strip()) > 0: # the required field
				buff.append(record)

	print categoryColor
	pdf.save()


if __name__ == '__main__':
	if len(sys.argv) != 2:
		print("USAGE: python %s <file.csv>" % sys.argv[0])
		exit(1)
	main()
