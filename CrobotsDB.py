#!/usr/bin/python -O
# -*- coding: UTF-8 -*-

"""
"CROBOTS" Crobots Batch Tournament Manager with DataBase support

Version:        Python/3.3

                Derived from Crobots.py 1.3

Author:         Maurizio Camangi

Version History:
                Version 3.3 No need of log files anymore
                Version 3.2 Return error code on SystemExit after Exception
                Version 3.1 Save match list into dbase using a custom key
                Version 3.0 Added support for Count Python
                Version 2.1 Added MySQL support - polish code
                Version 2.0.2 Polish code - use os.devnull
                Version 2.0 Use /run/user/{userid}/crobots as temp and log dir
                Version 1.2 Use shutil and glob to build log files
                Version 1.1 more compact iterations / combinations with
                start / end offset

                Version 1.0 is the first stable version

"""

import os.path
import shelve
import shlex
import subprocess
import sys
import time
from itertools import combinations
from random import shuffle

from Count import parse_log_file
from CrobotsLibs import available_cpu_count, check_stop_file_exist, clean_up_log_file, test_connection, \
    close_connection, \
    set_up, DATABASE_ENABLE, update_results, load_from_file, clean_up

# Global configuration variables

# databases
STATUS_KEY = '__STATUS__'
dbase = None

# command line strings
robotPath = "%s/%s.ro"
crobotsCmdLine = "crobots -m%s -l200000"
dbfile = "db/%s_%s.db"
matches = {'f2f': 2, '3vs3': 3, '4vs4': 4}

# if True overrides the Configuration class parameters
overrideConfiguration = False

# number of CPUs / cores
CPUs = available_cpu_count()
print "Detected %s CPU(s)" % CPUs
spawnList = []


def run_crobots(logtype):
    "spawn crobots command lines in subprocesses"
    global spawnList
    procs = []
    # spawn processes
    for s in spawnList:
        with open(os.devnull, 'w') as devnull:
            try:
                procs.append(subprocess.Popen(shlex.split(s), stdout=subprocess.PIPE, stderr=devnull))
            except OSError, e:
                raise SystemExit(e)
    # aggregate logs
    lines = []
    for proc in procs:
        output, unused_err = proc.communicate()
        for s in output.split('\n'):
            lines.append(s)
    update_db(lines, logtype)
    spawnList = []


def spawn_crobots_run(cmdLine, logtype):
    "put command lines into the buffer and run"
    global spawnList, CPUs
    spawnList.append(cmdLine)
    if len(spawnList) == CPUs:
        run_crobots(logtype)


def build_crobots_cmdline(paramCmdLine, robotList, logtype):
    "build and run crobots command lines"
    shuffle(robotList)
    spawn_crobots_run(" ".join([paramCmdLine] + robotList), logtype)


# initialize database
def init_db(logfile, logtype):
    global configuration, dbase, dbfile
    filename = dbfile % (logfile, logtype)
    if not os.path.exists(filename):
        print "Init local database for %s" % logtype.upper()
        dbase = shelve.open(filename, 'c')
        for s in configuration.listRobots:
            key = os.path.basename(s)
            dbase[key] = [0, 0, 0, 0]
        dbase.sync()
    else:
        dbase = shelve.open(filename, 'w')
    test_connection()


def close_db():
    global dbase
    if dbase is not None:
        try:
            dbase.close()
        except:
            print "Error on closing local database: results may be corrupted..."
        finally:
            dbase = None
    close_connection()


# initialize status
def init_status(logtype):
    global dbase
    if not STATUS_KEY in dbase:
        print "Init local status database for %s" % logtype.upper()
        l = list(combinations(configuration.listRobots, matches[logtype]))
        shuffle(l)
        dbase[STATUS_KEY] = l
        dbase.sync()
        set_up(logtype)


# update database
def update_db(lines, logtype):
    global dbase
    robots = parse_log_file(lines)
    for r in robots.values():
        name = r[0]
        values = dbase[name]
        values[0] += r[1]
        values[1] += r[2]
        values[2] += r[3]
        values[3] += r[4]
        dbase[name] = values
        if DATABASE_ENABLE:
            update_results(logtype, name, values[0], values[1], values[2], values[3])
    dbase.sync()


# save current status
def save_status(l):
    global dbase
    dbase[STATUS_KEY] = l
    dbase.sync()


# clean up database
def cleanup(logfile, logtype):
    global dbfile
    clean_up_log_file(dbfile % (logfile, logtype))
    print 'Clean up done %s %s' % (logfile, logtype.upper())


if len(sys.argv) <> 3:
    raise SystemExit('Usage : CrobotsDB.py <conf.py> [f2f|3vs3|4vs4|all|test|setup|clean]')

confFile = sys.argv[1]
action = sys.argv[2]

if not os.path.exists(confFile):
    raise SystemExit('Configuration file %s does not exist' % confFile)

if not action in ['f2f', '3vs3', '4vs4', 'all', 'test', 'setup', 'clean']:
    raise SystemExit('Invalid parameter %s. Valid values are f2f, 3vs3, 4vs4, all, test, setup, clean' % action)

try:
    configuration = load_from_file(confFile)
except Exception, e:
    raise SystemExit('Invalid configuration py file %s: %s' % (confFile, e))

if configuration is None:
    raise SystemExit('Invalid configuration py file %s' % confFile)

if len(configuration.listRobots) == 0:
    raise SystemExit('List of robots empty!')

if overrideConfiguration:
    print 'Override configuration...'
    configuration.label = 'test'
    configuration.matchF2F = 500
    configuration.match3VS3 = 8
    configuration.match4VS4 = 1
    configuration.sourcePath = 'test'

print 'List size = %d' % len(configuration.listRobots)
print 'Test opponents... ',

for r in configuration.listRobots:
    robot = robotPath % (configuration.sourcePath, r)
    if not os.path.exists(robot):
        raise SystemExit('Robot file %s does not exist.' % robot)

print 'OK!'

if action == 'clean':
    for a in ['f2f', '3vs3', '4vs4']:
        cleanup(configuration.label, a)
        if DATABASE_ENABLE: clean_up(a)
    close_db()
    raise SystemExit

if action == 'setup':
    for a in ['f2f', '3vs3', '4vs4']:
        cleanup(configuration.label, a)
        init_db(configuration.label, a)
        init_status(a)
    close_db()
    raise SystemExit

if action == 'test':
    test_connection()
    close_connection()
    print 'Test completed!'
    raise SystemExit

if check_stop_file_exist():
    print 'Crobots.stop file found! Exit application.'
    close_db()
    raise SystemExit


def run_tournament(ptype, matchParam):
    global robotPath, configuration, crobotsCmdLine
    print '%s Starting %s... ' % (time.ctime(), ptype.upper())
    param = crobotsCmdLine % matchParam
    init_db(configuration.label, ptype)
    init_status(ptype)
    match_list = dbase[STATUS_KEY]
    list_length = len(match_list)
    counter = 0
    while counter < list_length:
        if check_stop_file_exist():
            break
        build_crobots_cmdline(param, [robotPath % (configuration.sourcePath, s) for s in match_list.pop()], ptype)
        counter += 1
    if len(spawnList) > 0:
        run_crobots(ptype)
    if check_stop_file_exist():
        save_status(match_list)
        close_db()
        print 'Crobots.stop file found! Exit application.'
        raise SystemExit
    save_status(match_list)
    print '%s %s completed!' % (time.ctime(), ptype.upper())
    close_db()


if action in ['f2f', 'all']:
    run_tournament('f2f', configuration.matchF2F)

if action in ['3vs3', 'all']:
    run_tournament('3vs3', configuration.match3VS3)

if action in ['4vs4', 'all']:
    run_tournament('4vs4', configuration.match4VS4)

close_db()