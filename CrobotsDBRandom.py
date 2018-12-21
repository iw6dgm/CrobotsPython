#!/usr/bin/python -O
# -*- coding: UTF-8 -*-

"""
"CROBOTS" Crobots Batch Tournament Manager with DataBase support

Version:        Python/1.4

                Derived from Crobots.py 1.3

Author:         Maurizio Camangi

Version History:
                Version 1.4 Return error code on SystemExit after Exception
                Version 1.3 Count Python support
                Patch 1.2.2 Polish code
                Patch 1.2.1 Use os.devnull
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
from random import shuffle

from Count import parse_log_file
from CrobotsLibs import available_cpu_count, check_stop_file_exist, clean_up_log_file, load_from_file

# Global configuration variables
# databases
dbase = None

# command line strings
robotPath = "%s/%s.ro"
crobotsCmdLine = "crobots -m%s -l200000"
matches = {'3vs3': 3, '4vs4': 4}

# if True overrides the Configuration class parameters
overrideConfiguration = False

# number of CPUs / cores
CPUs = available_cpu_count()
print "Detected %s CPU(s)" % CPUs
spawnList = []
LIMIT = sys.maxint


def peek(l, n):
    shuffle(l)
    last = len(l) // n
    i = 0
    while i <= last:
        yield l[i:i + n]
        i += n
    return


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
    # shuffle(robotList)
    spawn_crobots_run(" ".join([paramCmdLine] + robotList))


# initialize database
def init_db(logfile, logtype):
    global configuration, startStatus, dbase
    dbfile = 'db/%s_%s.db' % (logfile, logtype)
    if not os.path.exists(dbfile):
        dbase = shelve.open(dbfile, 'c')
        for s in configuration.listRobots:
            key = os.path.basename(s)
            dbase[key] = [0, 0, 0, 0]
        dbase.sync()
        return 0
    else:
        dbase = shelve.open(dbfile, 'w')
        c = 0
        for r in dbase:
            values = dbase[r]
            c += values[0]
        return c


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
    global dbase
    if dbase is not None:
        try:
            dbase.close()
        except:
            print "Error on closing local database: results may be corrupted..."
        finally:
            dbase = None


# clean up database and status files
def cleanup(logfile, logtype):
    clean_up_log_file('db/%s_%s.db' % (logfile, logtype))
    print 'Clean up done %s %s!' % (logfile, logtype)


if len(sys.argv) <> 3:
    raise SystemExit("Usage : CrobotsDB.py <conf.py> [3vs3|4vs4|all|test|clean]")

confFile = sys.argv[1]
action = sys.argv[2]

if not os.path.exists(confFile):
    raise SystemExit('Configuration file %s does not exist' % confFile)

if action not in ['3vs3', '4vs4', 'all', 'test', 'clean']:
    raise SystemExit('Invalid parameter %s. Valid values are 3vs3, 4vs4, all, test, clean' % action)

if 'clean' != action and LIMIT < CPUs:
    raise SystemExit('Invalid match LIMIT: min value is %s' % CPUs)

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
    for a in ['3vs3', '4vs4']:
        cleanup(configuration.label, a)
    raise SystemExit

if action == 'test':
    print 'Test completed!'
    raise SystemExit

if check_stop_file_exist():
    print 'Crobots.stop file found! Exit application.'
    close_db()
    raise SystemExit


def run_tournament(ptype, matchParam):
    global countCmdLine, matches, tmppath, logpath, LIMIT
    print '%s Starting %s... ' % (time.ctime(), ptype.upper())
    param = crobotsCmdLine % matchParam
    temp = configuration.listRobots
    counter = init_db(configuration.label, ptype)
    print '%s matches found on db...' % counter
    n = matches[ptype]
    while (not check_stop_file_exist()) and (counter < LIMIT):
        for r in peek(temp, n):
            build_crobots_cmdline(param, [robotPath % (configuration.sourcePath, s) for s in r])
            counter += matchParam
            if counter >= LIMIT:
                break
    if check_stop_file_exist():
        print 'Crobots.stop file found! Exit application.'
        close_db()
        raise SystemExit
    print '%s %s completed!' % (time.ctime(), ptype.upper())
    close_db()


if action in ['3vs3', 'all']:
    run_tournament('3vs3', configuration.match3VS3)

if action in ['4vs4', 'all']:
    run_tournament('4vs4', configuration.match4VS4)

close_db()