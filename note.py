#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# note.py - an Apple iCloud client for Python environments
#
# Author: Ronald Copley <ronald@ronaldcopley.com>
# Copyright: GPLv3 (http://gplv3.fsf.org/)
# Feel free to use the code, but please share the changes you've made
# 

class note:
	def __init__(self, subject='', content='', created=None, modified=None):
		self.subject = subject
		self.content = content
		self.created = created
		self.modified = modified