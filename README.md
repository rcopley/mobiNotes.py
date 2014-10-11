mobiNotes.py
=========
Notes uploader for EasUS MobiSaver iPhone recovery tool
License: Copyleft GPLv3
Author: Ronald Copley <ronald@ronaldcopley.com>

Forked from Apple iNotes client written in Python on October 11th, 2014
iNotes.py Author: Xavier Mertens <xavier@rootshell.be>

Features
--------
* Search for existing notes
* List/count current notes

Shortfalls
----------
EaseUS MobiSaver outputs a human readable version of the notes you choose to recover as a single file. This makes it easy to read, but doesn't have any delimeter to seperate individual notes. To workaround this, we do a regex check for the header line of the note (\[note subject] \[timestamp] \[timestamp] \[note]).

Because of this, you may have trouble importing notes if they have a full timestamp in the note body.

Todo
----
* Implement sighandler
