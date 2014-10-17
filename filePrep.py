#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# fileprep.py - an Apple iCloud client for Python environments
#
# Author: Ronald Copley <ronald@ronaldcopley.com>
# Copyright: GPLv3 (http://gplv3.fsf.org/)
# Feel free to use the code, but please share the changes you've made
# 

import re
import fileinput
import sys
import time
import calendar
#import datetime
from datetime import datetime, timedelta
from optparse import OptionParser

#global filename

class note:
	def __init__(self, subject='', content='', created=None, modified=None):
		self.subject = subject
		self.content = content
		self.created = created
		self.modified = modified

def loadNotes(filename):
	# regex patern header line
	# Groups:
	#	subject, body, created, modified
	pattern = '(?P<subject>^.*)\t(?P<created>\d{4}-\d{2}-[0-3]\d [0-2]\d:[0-6]\d:[0-6]\d)\t(?P<modified>\d{4}-[0-1]\d-[0-3]\d [0-2]\d:[0-6]\d:[0-6]\d)\t(?P<body>.*)'

	notes = []
	currNote = None
	body = ''
	for line in fileinput.input(filename):
		noteHeader = re.search(pattern, line)
		if noteHeader!=None:
			#store existing note
			if currNote != None:
				currNote.content = body
				notes.append(currNote)
			currNote = None
			body = ''

			#read header
			#MobiSaver uses the local timezone on the phone in it's exports, however it truncates the timezone from the actual export
			#assume computer's local timezone unless overridden by program switch

			# if t>= 0:
			# 	#positive or zero utc offset
			# 	timezoneUTCOffset = "+"+"%04d"%t
			# else:
			# 	timezoneUTCOffset = "%05d"%t
			#gives a UTC timestamp
			createdTimestamp = datetime.strptime(noteHeader.group('created'), '%Y-%m-%d %H:%M:%S') + timedelta(seconds = -time.timezone)
			createdEpoch = calendar.timegm(createdTimestamp.timetuple())
			##DEBUG
			#createdEpoch = time.time()
			modifiedTimestamp = datetime.strptime(noteHeader.group('modified'), '%Y-%m-%d %H:%M:%S') + timedelta(seconds = -time.timezone)
			modifiedEpoch = calendar.timegm(modifiedTimestamp.timetuple())
			##DEBUG
			#modifiedEpoch = time.time()
			subject = noteHeader.group('subject')
			body = noteHeader.group('body')

			currNote = note(subject, body, createdEpoch, modifiedEpoch)
		else:
			body = body + line

	#store last note
	currNote.content = body
	notes.append(currNote)
	return notes

def main(argv):
	#global filename
	print 'fileprep parser test'
	print 'Author: Ronald Copley'
	print 'Released under GPLv3 on 10/13/2014\n'
	parser = OptionParser()
	parser.add_option('-f', '--file', action='store', type='string', dest='filename')
	(options, args) = parser.parse_args()

	print 'Loading file...'
	
	notes = loadNotes(options.filename)

	print "Printing Notes...\n"
	#print notes
	for n in notes:
		#print n
		print 'Created: '+n.created.strftime('%a, %d %b %Y %H:%M:%S %z')
		print 'Modified: '+n.modified.strftime('%a, %d %b %Y %H:%M:%S %z')
		print 'subject: '+n.subject
		print 'Body: (starts on next line)\n'+n.content
		print '================================================='

if __name__ == '__main__':
	main(sys.argv[1:])
	sys.exit()