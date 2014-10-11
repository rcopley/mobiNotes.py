#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# iNotes.py - an Apple iCloud client for Python environments
#
# Author: Xavier Mertens <xavier@rootshell.be>
# Copyright: GPLv3 (http://gplv3.fsf.org/)
# Feel free to use the code, but please share the changes you've made
# 

import imaplib
import time
import ConfigParser
import email.message
import os
import sys
import time
import getpass
import re
from optparse import OptionParser
from HTMLParser import HTMLParser

global debug 
global configFile
configFile = 'inotes.conf'

class MLStripper(HTMLParser):
	def __init__(self):
		self.reset()
		self.fed = []
	def handle_data(self, d):
		self.fed.append(d)
	def get_data(self):
		return ''.join(self.fed)

def removeHTMLTags(html):
	s = MLStripper()
	s.feed(html)
	return s.get_data()

def connectImap(configFile):
	# Read configuration file
	config = ConfigParser.ConfigParser()
	config.read(configFile)
	hostname = config.get('server', 'hostname')
	username = config.get('server', 'username')
	password = config.get('server', 'password')

	if password == '': password = getpass.getpass('iCloud Password: ')

	# Open an IMAP connection
	if debug: print '+++ Connecting to', hostname
	connection = imaplib.IMAP4_SSL(hostname)

	# Authenticate
	if debug: print '+++ Logging in as', username
	connection.login(username, password)
	return connection

def countNotes(connection, configFile):
	#c = connectImap(configFile)
	try:
		typ, data = connection.select('Notes', readonly=True)
		nbMsgs = int(data[0])
		print 'You have %d available notes.' % nbMsgs
	finally:
		print "leaving"
		# try:
		# 	connection.close()
		# except:
		# 	pass
		# connection.logout()
	return

def listNotes(connection, configFile):
	#c = connectImap(configFile)
	try:
		typ, data = connection.select('Notes', readonly=True)
		typ, [ids] = connection.search(None, 'ALL')
		for id in ids.split():
			typ, data = connection.fetch(id, '(RFC822)')
			for d in data:
				if isinstance(d, tuple):
					msg = email.message_from_string(d[1])
					print msg['subject']
	finally:
		# try:
		# 	connection.close()
		# except:
		# 	pass
		# connection.logout()
	return
def searchNotes(connection, configFile, queryString, stripHtml):
	#c = connectImap(configFile)
	try:
		typ, data = c.select('Notes', readonly=True)
		query = '(OR TEXT "%s" SUBJECT "%s")' % (queryString, queryString)
		typ, [ids] = c.search(None, query)
		for id in ids.split():
			#typ, data = c.fetch(id, '(RFC822)')
			typ, data = c.fetch(id, '(BODY[HEADER.FIELDS (SUBJECT)] BODY[TEXT])')
			#for d in data:
				#if isinstance(d, tuple):
					#msg = email.message_from_string([1])
					#print "Title:", msg['subject']
					#print msg
			print data[0][1].strip()
			print "---"
			if stripHtml:
				print removeHTMLTags(data[1][1])
			else:
				print data[1][1]
	finally:
		# try:
		# 	c.close()
		# except:
		# 	pass
		# c.logout()
	return

def createNote(connection, configFile, subject,savehtml):
	#c = connectImap(configFile)

	pattern = '(\d{4})-(0[1-9]|1[0-2]|[1-9])-(\3([12]\d|0[1-9]|3[01])|[1-9])[tT\s]([01]\d|2[0-3‌​])\:(([0-5]\d)|\d)\:(([0-5]\d)|\d)\t'

	try:
		# Read configuration file
		config = ConfigParser.ConfigParser()
		config.read(configFile)
		username = config.get('server', 'username')

		if debug: print "+++ Type your note and exit with CTRL-D"
		if savehtml:
			body = '<html>\n<head></head>\n<body>'
			for line in sys.stdin.readlines():
				body += line
				body += '<br>'
			body += '</body></html>'
		else:
			body = ''
			for line in sys.stdin.readlines():
				body += line

		now = time.strftime('%a, %d %b %Y %H:%M:%S %z')
		note = "Date: %s\nFrom: %s@me.com\nX-Uniform-Type-Identifier: com.apple.mail-note\nContent-Type: text/html;\nSubject: %s\n\n%s" % (now, username, subject, body)
		c.append('Notes', '', imaplib.Time2Internaldate(time.time()), str(note))
		
	finally:
		# try:
		# 	c.close()
		# except:
		# 	pass
		# c.logout()
	
	return

def main(argv):
	global debug
	global configFile
	debug = 0

	parser = OptionParser(usage="usage: %prog [options]", version="%prog 1.0")
	parser.add_option('-c', '--config', dest='configFile', type='string', \
		help='specify the configuration file')
	parser.add_option('-C', '--count', action='store_true', dest='count', \
		help='count the number of notes')
	parser.add_option('-d', '--debug', action='store_true', dest='debug', \
		help='display this message', default='False')
	parser.add_option('-H', '--html', action='store_true', dest='saveHtml', \
		help='save the new note in HTML format')
	parser.add_option('-l', '--list', action='store_true', dest='list', \
		help='list saved notes')
	parser.add_option('-q', '--query', dest='query', type='string', \
		help='search fo keyword in saved notes')
	parser.add_option('-s', '--subject', dest='subject', type='string', \
		help='create a new note with subject')
	parser.add_option('-S', '--striphtml', action='store_true', dest='stripHtml', \
		help='remove HTML tags from displayed notes')
	(options, args) = parser.parse_args()
	if options.debug == True:
		debug = 1
		print '+++ Debug mode'
	if options.configFile == None:
		if not os.path.isfile(configFile):
			print 'Cannot open ' + configFile + '. Use the -c switch to provide a valid configuration.'
			sys.exit(1)
	else:
		configFile = options.configFile
	if debug: print '+++ Configuration file:', configFile
	
	connection = connectImap(configFile)

	if options.count == True:
		countNotes(connection, configFile)
	elif options.list == True:
		listNotes(connection, configFile)
	elif options.query != None:
		searchNotes(connection, configFile, options.query, options.stripHtml)
	else:
		createNote(connection, configFile, options.subject, options.saveHtml)

	# Wrapping up
	try:
		connection.close()
	except:
		pass
	connection.logout()

if __name__ == '__main__':
	main(sys.argv[1:])
	sys.exit()
