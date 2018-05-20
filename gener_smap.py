#! /usr/bin/python3

# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# application: EMPER simulator
# brief: economic and strategic simulator
# opensource licence: GPL-3.0

from time import time
start_time = time() 

import sys, os
import sqlite3

from tools import print_out
from tools import print_info
from tools import print_error

from EmperSQL import EmperSQL


if len(sys.argv) < 4:
    print_error("USAGE: %s <database> <source> <formula>..." % sys.argv[0])
    raise ValueError("wrong args number")

formulae = {}
for kv in sys.argv[3:]:
    k,v = kv.split(":")
    formulae[k] = float(v)

handler = EmperSQL(sys.argv[1])

query = "SELECT name FROM population"
nodes = handler.select_many(query)

for nodename in nodes:
    pnum = handler.calc_points(nodename)
    if pnum == 0:
        print_error("NO NODE: %s (%s)" % (sys.argv[2], nodename[0]))
        raise ValueError("wrong arg")

    mass = 0.0
    for xy in  handler.nodepoints_generator(nodename[0]):
        try:
            if formulae["BUILDABLE"] > 0.5:
                if not handler.is_buildable(*xy):
                    break
            if formulae["BUILDABLE"] < 0.5:
                if handler.is_buildable(*xy):
                    break
        except KeyError: pass
        
        color = handler.diagram[xy][1]
        try:
            mass += formulae[color]
        except KeyError: pass
        try:
            if handler.is_coast(*xy):
                mass += formulae["COAST"]
        except KeyError: pass

    value = mass/pnum
    args = (sys.argv[2], value, nodename[0])
    handler.execute("UPDATE sources set %s=%g WHERE name='%s'" % args)
    print_out("%s: %g" % (nodename[0], value))

    
del handler

stop_time = time()
delta_time = stop_time - start_time     
print_info("duration: %.3f s" % delta_time)

