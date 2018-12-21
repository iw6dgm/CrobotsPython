#!/usr/bin/python -O
# -*- coding: UTF-8 -*-

"""
"CROBOTS" Crobots Batch Bench Manager to test one single robot with DataBase
  support

Version:        Python/1.5

                Derived from CrobotsDB.py 1.1 and CrobotsBench.py 1.0

Author:         Maurizio Camangi

Version History:
                Version 1.5 No need of log files anymore
                Version 1.4 Return error code on SystemExit after Exception
                Version 1.3 Save match list into dbase using a custom key
                Version 1.2 Count Python support - polish code
                Patch 1.1.1 Use os.devnull
                Version 1.1 Use shutil and glob to build log files
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

from CrobotsLibs import available_cpu_count, check_stop_file_exist, load_from_file, clean_up_log_file
from Count import parse_log_file

# Global configuration variables
# databases
dbfilename = 'db/%s_%s_%s.db'
STATUS_KEY = '__STATUS__'
dbase = None
matches = {'f2f': 1, '3vs3': 2, '4vs4': 3}

# command line strings
robotPath = "%s/%s.ro"
crobotsCmdLine = "crobots -m%s -l200000 %s"

# if True overrides the Configuration class parameters
overrideConfiguration = False

# number of CPUs / cores
CPUs = available_cpu_count()
print "Detected %s CPU(s)" % CPUs
spawnList = []


def run_crobots():
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
    update_db(lines)
    spawnList = []


def spawn_crobots_run(cmdLine):
    "put command lines into the buffer and run"
    global spawnList, CPUs
    spawnList.append(cmdLine)
    if len(spawnList) == CPUs:
        run_crobots()


def build_crobots_cmdline(paramCmdLine, robotList):
    "build and run crobots command lines"
    shuffle(robotList)
    spawn_crobots_run(" ".join([paramCmdLine] + robotList))


# initialize database
def init_db(logfile, logtype):
    global configuration, startStatus, dbase, robotTest, dbfilename
    robotname = os.path.basename(robotTest)[:-3]
    dbfile = dbfilename % (logfile, robotname, logtype)
    if not os.path.exists(dbfile):
        dbase = shelve.open(dbfile, 'c')
        dbase[robotname] = [0, 0, 0, 0]
        for s in configuration.listRobots:
            key = os.path.basename(s)
            dbase[key] = [0, 0, 0, 0]
        dbase.sync()
    else:
        dbase = shelve.open(dbfile, 'w')


# update database
def update_db(lines):
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
    dbase.sync()


def close_db():
    global dbase, dbstatus
    if dbase is not None:
        try:
            dbase.close()
        except:
            print "Error on closing local database: results may be corrupted..."
        finally:
            dbase = None


# initialize status
def init_status(logtype):
    global dbase
    if not STATUS_KEY in dbase:
        print "Init local status database for %s" % logtype.upper()
        l = list(combinations(configuration.listRobots, matches[logtype]))
        shuffle(l)
        dbase[STATUS_KEY] = l
        dbase.sync()


# save current status
def save_status(l):
    global dbase
    dbase[STATUS_KEY] = l
    dbase.sync()


# clean up database and status files
def cleanup(logfile, logtype):
    global dbfilename, robotTest
    robotname = os.path.basename(robotTest)[:-2]
    clean_up_log_file(dbfilename % (logfile, robotname, logtype))
    print 'Clean up done %s %s %s!' % (logfile, robotname, logtype)


if len(sys.argv) <> 4:
    raise SystemExit("Usage : CrobotsBenchDB.py <conf.py> <robot.r> [f2f|3vs3|4vs4|all|test|clean]")

confFile = sys.argv[1]
robotTest = sys.argv[2]
action = sys.argv[3]


if not os.path.exists(confFile):
    raise SystemExit('Configuration file %s does not exist' % confFile)

if not action in ['f2f', '3vs3', '4vs4', 'all', 'test', 'clean']:
    raise SystemExit('Invalid parameter %s. Valid values are f2f, 3vs3, 4vs4, all, test, clean' % action)

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
    raise SystemExit

if not os.path.exists(robotTest):
    raise SystemExit('Robot %s does not exist' % robotTest)
else:
    print 'Compiling %s ...' % robotTest,
    clean_up_log_file(robotTest + 'o')
    with open(os.devnull, 'w') as devnull:
        try:
            p = subprocess.Popen(shlex.split("crobots -c %s" % robotTest), stdout=devnull, stderr=devnull, close_fds=True)
            p.communicate()
        except Exception, e:
            raise SystemExit('Error on compiling Robot %s: %s' % (robotTest, e))
    if not os.path.exists(robotTest + 'o'):
        raise SystemExit('Robot %s does not compile' % robotTest)

print 'OK!'
robotTest += 'o'

if action == 'test':
    print 'Test completed!'
    raise SystemExit


if check_stop_file_exist():
    print 'Crobots.stop file found! Exit application.'
    close_db()
    raise SystemExit


def run_tournament(ptype, matchParam):
    global dbase, robotPath, robotTest, configuration, crobotsCmdLine
    print '%s Starting %s... ' % (time.ctime(), ptype.upper())
    param = crobotsCmdLine % (matchParam, robotTest)
    init_db(configuration.label, ptype)
    init_status(ptype)
    match_list = dbase[STATUS_KEY]
    list_length = len(match_list)
    counter = 0
    while counter < list_length:
        if check_stop_file_exist():
            break

        build_crobots_cmdline(param, [robotPath % (configuration.sourcePath, s) for s in match_list.pop()])
        counter += 1
    if len(spawnList) > 0:
        run_crobots()
    if check_stop_file_exist():
        save_status(match_list)
        close_db()
        print 'Crobots.stop file found! Exit application.'
        raise SystemExit
    save_status(match_list)
    print '%s %s completed!' % (time.ctime(), ptype.upper())


if action in ['f2f', 'all']:
    run_tournament('f2f', configuration.matchF2F)

if action in ['3vs3', 'all']:
    run_tournament('3vs3', configuration.match3VS3)

if action in ['4vs4', 'all']:
    run_tournament('4vs4', configuration.match4VS4)


close_db()
