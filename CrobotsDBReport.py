#!/usr/bin/python -O
# -*- coding: UTF-8 -*-

"""
CrobotsDBReport v.1.1 - Given a dbase shows an ordered ranking

        v.1.0       Accepts one database only
        v.1.0.2     Specify db type (f2f, 3vs3, 4vs4) or all
        v.1.1       Support for balanced scoring systems
"""



import os.path
import shelve
import sys

__author__ = 'joshua'

from Count import print_report, schema4

STATUS_KEY = '__STATUS__'


def show_db_all_report(dbfile):
    if not os.path.exists('%s_f2f.db' % dbfile):
        raise SystemExit('DB %s_f2f.db does not exist. Exit.' % dbfile)
    dbase_f2f = shelve.open('%s_f2f.db' % dbfile, 'r')

    if not os.path.exists('%s_3vs3.db' % dbfile):
        raise SystemExit('DB %s_3vs3.db does not exist. Exit.' % dbfile)
    dbase_3vs3 = shelve.open('%s_3vs3.db' % dbfile, 'r')

    if not os.path.exists('%s_4vs4.db' % dbfile):
        raise SystemExit('DB %s_4vs4.db does not exist. Exit.' % dbfile)
    dbase_4vs4 = shelve.open('%s_4vs4.db' % dbfile, 'r')

    robots = []

    for r in dbase_f2f:
        if STATUS_KEY == r:
            continue
        values_f2f = dbase_f2f[r]
        values_3vs3 = dbase_3vs3[r]
        values_4vs4 = dbase_4vs4[r]
        games = values_f2f[0] + values_3vs3[0] + values_4vs4[0]
        wins = values_f2f[1] + values_3vs3[1] + values_4vs4[1]
        ties2 = values_f2f[2] + values_3vs3[2] + values_4vs4[2]
        ties3 = values_3vs3[3] + values_4vs4[3]
        ties4 = values_4vs4[4]
        points_f2f = (values_f2f[1] * schema4['f2f'][0])+(values_f2f[2] * schema4['f2f'][1])
        points_3vs3 = (values_3vs3[1] * schema4['3vs3'][0])+(values_3vs3[2] * schema4['3vs3'][1])+(values_3vs3[3] * schema4['3vs3'][2])
        points_4vs4 = (values_4vs4[1] * schema4['4vs4'][0])+(values_4vs4[2] * schema4['4vs4'][1])+(values_4vs4[3] * schema4['4vs4'][2])+(values_4vs4[4] * schema4['4vs4'][3])
        eff_f2f = 0.0
        if values_f2f[0] != 0:
            eff_f2f = 100.0 * points_f2f / (schema4['f2f'][0] * values_f2f[0])
        eff_3vs3 = 0.0
        if values_3vs3[0] != 0:
            eff_3vs3 = 100.0 * points_3vs3 / (schema4['3vs3'][0] * values_3vs3[0])
        eff_4vs4 = 0.0
        if values_4vs4[0] != 0:
            eff_4vs4 = 100.0 * points_4vs4 / (schema4['4vs4'][0] * values_4vs4[0])
        eff = (eff_f2f + eff_3vs3 + eff_4vs4) / 3.0

        robots.append([r, games, wins, ties2, ties3, ties4, games - wins - (ties2+ties3+ties4), points_f2f+points_3vs3+points_4vs4, eff])

    dbase_f2f.close()
    dbase_3vs3.close()
    dbase_4vs4.close()
    print_report(robots)


def show_db_report(dbfile, dbtype):
    if not os.path.exists(dbfile):
        raise SystemExit('DB %s does not exist. Exit.' % dbfile)
    robots = []
    dbase = shelve.open(dbfile, 'r')
    for r in dbase:
        if STATUS_KEY == r:
            continue
        values = dbase[r]
        games = values[0]
        wins = values[1]
        ties2 = values[2]
        ties3 = values[3]
        ties4 = values[4]
        eff = 0.0
        points = (wins * schema4[dbtype][0])+(ties2 * schema4[dbtype][1])+(ties3 * schema4[dbtype][2])+(ties4 * schema4[dbtype][3])
        if games != 0:
            eff = 100.0 * points / (schema4[dbtype][0] * games)
        robots.append([r, games, wins, ties2, ties3, ties4, games - wins - (ties2+ties3+ties4), points, eff])
    dbase.close()
    print_report(robots)


def main():
    if len(sys.argv) <> 3:
        print "Usage : CrobotsDBReport.py <dbfile prefix> [f2f|3vs3|4vs4|all]"
        raise SystemExit
    dbfile = sys.argv[1]
    dbtype = sys.argv[2]
    if dbtype == 'all':
        show_db_all_report(dbfile)
    else:
        show_db_report("%s_%s.db" % (dbfile, dbtype), dbtype)

if __name__ == '__main__':
    main()
