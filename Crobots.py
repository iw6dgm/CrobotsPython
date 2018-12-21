#!/usr/bin/python -O
# -*- coding: UTF-8 -*-

"""
"CROBOTS" Crobots Batch Tournament Manager

Version:        Python/1.7

                Translated from 'run2012.sh' UNIX/bash to Python 2.7

Author:         Maurizio Camangi

Version History:
                Version 1.7 No need of log files anymore
                Version 1.6 Return error code on SystemExit after Exception
                Version 1.5 Count Python support
                Version 1.4.2 Polish code - use os.devnull - no more </dev/null needed
                Patch 1.3.1 Fix import
                Version 1.3 Use more compact build_crobots_cmdline function

                Version 1.2 Use more compact combinations from itertools

                Version 1.1 is the first stable version
                (corresponds to bash/v.1.2c)

                Add multiple CPUs / cores management

"""

import os.path
import shlex
import subprocess
import sys
import time
from itertools import combinations
from random import shuffle

import CrobotsLibs
from Count import parse_log_file, show_report
from CrobotsLibs import available_cpu_count, check_stop_file_exist

# Global configuration variables
# databases
dbase = None

# command line strings
robotPath = "%s/%s.ro"
crobotsCmdLine = "crobots -m%s -l200000"

# if True overrides the Configuration class parameters
overrideConfiguration = False

# number of CPUs / cores
CPUs = available_cpu_count()
print "Detected %s CPU(s)" % CPUs
spawnList = []


# initialize database
def init_db():
    global configuration, dbase
    dbase = dict()
    for s in configuration.listRobots:
        key = os.path.basename(s)
        dbase[key] = [key, 0, 0, 0, 0]


# update database
def update_db(lines):
    global dbase
    robots = parse_log_file(lines)
    for r in robots.values():
        name = r[0]
        values = dbase[name]
        values[0] = name
        values[1] += r[1]
        values[2] += r[2]
        values[3] += r[3]
        values[4] += r[4]
        dbase[name] = values


def run_crobots():
    """spawn crobots command lines in subprocesses"""
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
    """put command lines into the buffer and run"""
    global spawnList, CPUs
    spawnList.append(cmdLine)
    if len(spawnList) == CPUs:
        run_crobots()


def build_crobots_cmdline(paramCmdLine, robotList):
    """build and run crobots command lines"""
    shuffle(robotList)
    spawn_crobots_run(" ".join([paramCmdLine] + robotList))


if len(sys.argv) <> 3:
    raise SystemExit("Usage : Crobots.py <conf.py> [f2f|3vs3|4vs4|all|test]")

confFile = sys.argv[1]
action = sys.argv[2]

if not os.path.exists(confFile):
    raise SystemExit('Configuration file %s does not exist' % confFile)

if not action in ['f2f', '3vs3', '4vs4', 'all', 'test']:
    raise SystemExit('Invalid parameter %s. Valid values are f2f, 3vs3, 4vs4, all, test' % action)

try:
    configuration = CrobotsLibs.load_from_file(confFile)
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
    if not os.path.exists(os.path.normpath(robot)):
        raise SystemExit('Robot file %s does not exist.' % robot)

print 'OK!'

if action == 'test':
    print 'Test completed!'
    raise SystemExit


def run_tournament(ptype, num, matchParam):
    global tmppath, logpath, robotPath, configuration, crobotsCmdLine
    print '%s Starting %s... ' % (time.ctime(), ptype.upper())
    init_db()
    param = crobotsCmdLine % matchParam
    for r in combinations(configuration.listRobots, num):
        if check_stop_file_exist():
            print 'Crobots.stop found! Exit application.'
            raise SystemExit
        build_crobots_cmdline(param, [robotPath % (configuration.sourcePath, s) for s in r])
    if len(spawnList) > 0: run_crobots()
    show_report(dbase)
    print '%s %s completed!' % (time.ctime(), ptype.upper())


if action in ['f2f', 'all']:
    run_tournament('f2f', 2, configuration.matchF2F)

if action in ['3vs3', 'all']:
    run_tournament('3vs3', 3, configuration.match3VS3)

if action in ['4vs4', 'all']:
    run_tournament('4vs4', 4, configuration.match4VS4)
