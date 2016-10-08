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
heading = copy.deepcopy(styleSheet['Heading1'])
heading.fontSize += 2

italic = copy.deepcopy(styleSheet['Italic'])
italic.fontSize += 2

smallItalic = copy.deepcopy(styleSheet['Italic'])

# colorsForTeams = [
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
	colorsForTeams = colors.getAllNamedColors().values()
	for k in allColors.keys():
		for unwantedName in ['white', 'yellow', 'CMYK', 'black', 'transparent']:
			if k.find(unwantedName) > -1: 
				print "removing %s" % k
				if allColors[k] in colorsForTeams:
					colorsForTeams.remove(allColors[k])
	return colorsForTeams

colorsForTeams = printableColors()
teamColor = {}

def valFor(record, key):
	return "%s: %s" % (key, record[key]) if record[key] else ''

def colorizeTeam(teamName):
	teamStyle = copy.deepcopy(italic)
	if len(teamColor) + 1 > len(colorsForTeams):
		print "Warning: more team names than colors defined, will repeat."
	if teamName not in teamColor:
		teamColor[teamName] = colorsForTeams[len(teamColor) % len(colorsForTeams)]
	teamStyle.textColor = teamColor[teamName]
	return teamStyle

def drawOnePage(pdf, records):
	# all in inches
	margin = 0.5
	printable_width = 7.5
	each_printable_height = 9.0 / NUM_PER_PAGE


	for i, record in enumerate(records):
		# see reportlab-userguide.pdf page 62.
		story = []
		story.append(Paragraph(str(record['Idea']), heading))
		story.append(Spacer(0,.5*inch))

		teamStyle = colorizeTeam(record['Team Focus'])
		story.append(Paragraph(valFor(record, 'Team Focus'), teamStyle))
		
		#debugging colors i don't want and need to exclude
		# story.append(Paragraph(str(teamStyle.textColor), italic))
		
		story.append(Paragraph(valFor(record, 'Bucket'), italic))
		story.append(Paragraph(str(record['Internal / External']), italic))
		story.append(Paragraph(valFor(record, 'JTBD'), italic))
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
			if len(record['Idea'].strip()) > 0:
				buff.append(record)

	print teamColor
	pdf.save()


if __name__ == '__main__':
	if len(sys.argv) != 2:
		print("USAGE: python %s <file.csv>" % sys.argv[0])
		exit(1)
	main()
