#!/usr/bin/python -O
# -*- coding: UTF-8 -*-

"""
"CROBOTS" Crobots Batch Bench Manager to test one single robot

Version:        Python/1.4

                Derived from Crobots.py 1.3.1

Author:         Maurizio Camangi

Version History:
                Version 1.4 Return error code on SystemExit after Exception
                Version 1.3 Count Python support
                Version 1.2 Use /run/user as log and tmp directory
                Patch 1.1.1 Use os.devnull
                Version 1.1 Use shutil and glob to build log files
                Version 1.0 is the first stable version

"""

import os.path
import shlex
import subprocess
import sys
import time
from itertools import combinations
from random import shuffle

from Count import parse_log_file, show_report
from CrobotsLibs import available_cpu_count, check_stop_file_exist, clean_up_log_file, load_from_file

# Global configuration variables
# databases
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


# initialize database
def init_db(test):
    global configuration, dbase
    dbase = dict()
    robotname = os.path.basename(test)[:-3]
    dbase[robotname] = [robotname, 0, 0, 0, 0]
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
    "spawn crobots command lines in subprocesses"
    global spawnList
    procs = []
    # spawn processes
    for s in spawnList:
        with open(os.devnull, 'w') as devnull:
            try:
                procs.append(subprocess.Popen(shlex.split(s), stdout=subprocess.PIPE, stderr=devnull, close_fds=True))
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


if len(sys.argv) <> 4:
    raise SystemExit("Usage : CrobotsBench.py <conf.py> <robot.r> [f2f|3vs3|4vs4|all|test]")

confFile = sys.argv[1]
robotTest = sys.argv[2]
action = sys.argv[3]


if not os.path.exists(confFile):
    raise SystemExit('Configuration file %s does not exist' % confFile)

if not action in ['f2f', '3vs3', '4vs4', 'all', 'test']:
    raise SystemExit('Invalid parameter %s. Valid values are f2f, 3vs3, 4vs4, all, test' % action)

try:
    configuration = load_from_file(confFile)
except Exception, e:
    raise SystemExit('Invalid configuration py file %s: %s' % (confFile, e))

if configuration == None:
    raise SystemExit('Invalid configuration py file %s' % confFile)

if len(configuration.listRobots) == 0:
    raise SystemExit('List of robots empty!')

if overrideConfiguration:
    print 'Override configuration...'
    #configuration.label = 'test'
    configuration.matchF2F = 10
    configuration.match3VS3 = 8
    configuration.match4VS4 = 1
    configuration.sourcePath = '.'

print 'List size = %d' % len(configuration.listRobots)
print 'Test opponents... ',

for r in configuration.listRobots:
    robot = robotPath % (configuration.sourcePath, r)
    if not os.path.exists(robot):
        raise SystemExit('Robot file %s does not exist.' % robot)

print 'OK!'

if not os.path.exists(robotTest):
    raise SystemExit('Robot %s does not exist' % robotTest)
else:
    print 'Compiling %s ...' % robotTest,
    clean_up_log_file(robotTest + 'o')
    with open(os.devnull, 'w') as devnull:
        try:
            p = subprocess.Popen(shlex.split("crobots -c %s" % robotTest), stdout=devnull, stderr=devnull)
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


def run_tournament(ptype, matchParam):
    global robotTest
    print '%s Starting %s... ' % (time.ctime(), ptype.upper())
    init_db(robotTest)
    param = crobotsCmdLine % (matchParam, robotTest)
    for r in combinations(configuration.listRobots, matches[ptype]):
        if check_stop_file_exist():
            print 'Crobots.stop found! Exit application.'
            raise SystemExit
        build_crobots_cmdline(param, [robotPath % (configuration.sourcePath, s) for s in r])
    if len(spawnList) > 0:
        run_crobots()
    show_report(dbase)
    print '%s %s completed!' % (time.ctime(), ptype.upper())

if action in ['f2f', 'all']:
    run_tournament('f2f', configuration.matchF2F)

if action in ['3vs3', 'all']:
    run_tournament('3vs3', configuration.match3VS3)

if action in ['4vs4', 'all']:
    run_tournament('4vs4', configuration.match4VS4)
