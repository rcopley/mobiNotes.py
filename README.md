mobiNotes.py
=========
Notes uploader for EasUS MobiSaver iPhone recovery tool
License: Copyleft GPLv3
Author: Ronald Copley <ronald@ronaldcopley.com>

Forked from Apple iNotes client written in Python on October 11th, 2014
iNotes.py Author: Xavier Mertens <xavier@rootshell.be>

Instructions
------------
To run this application, execute `mobiNotes.py` from the commandline, you must specify an input file with the `-f` option

Example
-------
To run this application, you must create the config file needed to login to iCloud. You can copy or rename the sample config file `inotes.cfg.sample` to `inotes.cfg` to get started right away. Entering your username and password into the configuration file is optional. It is recommended that you do not enter your password into the config file, unless neccesarry. If you do not enter a username and/or password in the config file, you will be prompted for it when you run the script.
    mobiNotes.py -f ~/notes.txt

You can specify the config file for the script to use with the `-c` switch. For example:
    mobiNotes.py -c myawesomeconfig.cfg -f ~/notes.txt

Features
--------
* Search for existing notes
* List/count current notes

Shortfalls
----------
EaseUS MobiSaver outputs a human readable version of the notes you choose to recover as a single file. This makes it easy to read, but doesn't have any delimeter to seperate individual notes. To workaround this, we do a regex check for the header line of the note (\[note subject] \[timestamp] \[timestamp] \[note]).

Because of this, you may have trouble importing notes if they have a full timestamp in the note body.

Command Line Options
--------------------
    Usage: mobiNotes.py [options]
    
    Options:
      --version             show program's version number and exit
      -h, --help            show this help message and exit
      -c CONFIGFILE, --config=CONFIGFILE
                            specify the configuration file
      -C, --count           count the number of notes
      -d, --debug           display this message
      -H, --html            save the new note in HTML format (default)
      -p, --plain           save the new note in HTML format (negates -H)
      -l, --list            list saved notes
      -q QUERY, --query=QUERY
                            search fo keyword in saved notes
      -s SUBJECT, --subject=SUBJECT
                            create a new note with subject
      -S, --striphtml       remove HTML tags from displayed notes
      -f FILENAME, --file=FILENAME
                            specifies the file to use for bulk note import
Todo
----
* Implement sighandler
