#!/usr/bin/python -O
# -*- coding: UTF-8 -*-

"""
Count Crobots log parser

Version:        Python/2.0

                Derived from Count 8.x

Author:         Maurizio Camangi

Version History:
                Version 2.0 Support for balanced scoring systems
                Patch 1.0.1 Fix wrong efficiency formula and 40% tie rule
                1.0 First stable version - just only parse a Crobots log and calculates matches
                No sorted ranking - no TXT / HTML output

"""


import os
import sys

__author__ = 'iw6dgm'

schema4 = {
'f2f' : [2, 1, 0, 0],
'3vs3': [3, 1, 1, 0],
'4vs4': [4, 1, 1, 1]
}

def compare(a, b):
    if a[8] > b[8]:
        return 1
    elif a[8] < b[8]:
        return -1
    return 0


def print_report(robots):
    robots.sort(compare, None, True)
    print '#\tName\t\tGames\t\tWins\t\tTies2\t\tTies3\t\tTies4\t\tLost\t\tPoints\t\tEff%'
    i = 0
    for values in robots:
        i += 1
        print '%i\t%s\t\t%i\t\t%i\t\t%i\t\t%i\t\t%i\t\t%i\t\t%i\t\t%.3f' % (i, values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7], values[8])


def show_report(db, type):
    robots = []
    for r in db.values():
        name = r[0]
        games = r[1]
        wins = r[2]
        ties2 = r[3]
        ties3 = r[4]
        ties4 = r[5]
        points = (wins * schema4[type][0])+(ties2 * schema4[type][1])+(ties3 * schema4[type][2])+(ties4 * schema4[type][3])
        eff = 0.0
        if games != 0:
            eff = 100.0 * points / (schema4[type][0] * games)
        robots.append([name, games, wins, ties2, ties3, ties4, games - wins - (ties2+ties3+ties4), points, eff])
    print_report(robots)


def get_name(row):
    n = row.strip(' ')
    if n[0] == '/':
        n = n[1:]
    return n


def get_survivor(row):
    """Name, Games, Wins, Tie2, Tie3, Tie4"""
    return [get_name(row[7:18]), int(row[31:33]), 0, 0, 0, 0]


def get_robot(row, db):
    n = get_name(row[7:18])
    if n in db:
        rob = db[n]
    else:
        """Name, Games, Wins, Tie2, Tie3, Tie4"""
        rob = [n, 0, 0, 0, 0, 0]
    rob[1] += 1
    return rob


def update_robot(row, survivors, db):
    rob = get_robot(row, db)
    name = rob[0]
    if name in survivors:
        surv = survivors[name]
        rob[2] += surv[2]
        rob[3] += surv[3]
        rob[4] += surv[4]
        rob[5] += surv[5]
    db[name] = rob


def update_survivor(row, survivors):
    srv = get_survivor(row)
    survivors[srv[0]] = srv


def parse_log_file(lines):
    robots = dict()
    for line in lines:
        l = len(line)
        if l < 2:
            continue
        elif 'Match' == line[0:5]:
            survivors = dict()
        elif 'damage=%' in line:
            if l < 50:
                update_survivor(line, survivors)
            else:
                tab = line.index('\t', 0, 50)
                update_survivor(line[:tab], survivors)
                update_survivor(line[tab + 1:], survivors)
        elif 'Cumulative' == line[2:12]:
            s = len(survivors) + 1
            if s == 1:
                continue
            for srv in survivors.values():
                srv[s] = 1
        elif 'wins=' in line:
            if l < 50:
                update_robot(line, survivors, robots)
            else:
                tab = line.index('\t', 0, 50)
                update_robot(line[:tab], survivors, robots)
                update_robot(line[tab + 1:], survivors, robots)
    return robots


def main():
    if len(sys.argv) != 3:
        print "Usage : Count.py <logfile> <type>"
        raise SystemExit

    logFile = sys.argv[1]
    type = sys.argv[2]

    if not os.path.exists(logFile):
        print 'Log file %s does not exist' % logFile
        raise SystemExit

    txt = open(logFile, 'r')
    lines = txt.readlines()
    txt.close()
    robots = parse_log_file(lines)
    show_report(robots, type)


if __name__ == '__main__':
    main()
