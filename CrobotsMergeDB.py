#!/usr/bin/python -O
# -*- coding: UTF-8 -*-

"""
"CROBOTS" Crobots Merge DataBase support

Version:        Python/1.1

                Derived from CrobotsDB.py 1.0

Author:         Maurizio Camangi

Version History:
                Version 1.1 i 'move' action: merge + clean sources
                Version 1.0 is the first stable version

"""

import os.path
import shelve
import sys

STATUS_KEY = '__STATUS__'


# update database
def merge_db():
    global dbaseout, dbase1, dbase2
    dbout = shelve.open(dbaseout, 'c')
    dbin1 = shelve.open(dbase1, 'r')
    dbin2 = shelve.open(dbase2, 'c')
    for key in dbin1:
        if STATUS_KEY == key:
            continue
        newvalues = dbin1[key]
        if key in dbout:
            values = dbout[key]
            values[0] += newvalues[0]
            values[1] += newvalues[1]
            values[2] += newvalues[2]
            values[3] += newvalues[3]
            dbout[key] = values
        else:
            dbout[key] = newvalues

        if key in dbin2:
            newvalues = dbin2[key]
            values = dbout[key]
            values[0] += newvalues[0]
            values[1] += newvalues[1]
            values[2] += newvalues[2]
            values[3] += newvalues[3]
            dbout[key] = values
    for key in dbin2:
        if STATUS_KEY == key:
            continue

        if key not in dbin1:
            newvalues = dbin2[key]
            if key in dbout:
                values = dbout[key]
                values[0] += newvalues[0]
                values[1] += newvalues[1]
                values[2] += newvalues[2]
                values[3] += newvalues[3]
                dbout[key] = values
            else:
                dbout[key] = newvalues
    dbout.sync()
    dbout.close()
    dbin1.close()
    dbin2.close()


# clean up database and status files
def cleanup(filepath):
    try:
        os.remove(filepath)
    except:
        pass
    print 'Clean up done %s!' % filepath


if len(sys.argv) <> 5:
    raise SystemExit("Usage : CrobotsMergeDB.py <db1> <db2> <dbout> [merge|move|clean]")

dbase1 = sys.argv[1]
dbase2 = sys.argv[2]
dbaseout = sys.argv[3]
action = sys.argv[4]

if not os.path.exists(dbase1):
    raise SystemExit('Source database does not exist')

if not action in ['merge', 'move', 'clean']:
    raise SystemExit('Invalid parameter %s. Valid values are [merge|move|clean]' % action)

if action == 'clean':
    cleanup(dbaseout)
    raise SystemExit

if action == 'merge':
    merge_db()
    print 'Merge done!'
    raise SystemExit

if action == 'move':
    merge_db()
    cleanup(dbase1)
    cleanup(dbase2)
    raise SystemExit
