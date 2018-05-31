#! /usr/bin/python3

# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# application: EMPER simulator
# brief: economic and strategic simulator
# opensource licence: GPL-3.0

from time import time
start_time = time() 

import math
import sys, os
from tools import *
from EmperSQL import EmperSQL


if len(sys.argv) < 4:
    print_error("USAGE: %s <database> <source> <formula>..." % sys.argv[0])
    raise ValueError("wrong args number")

formulae = {}
for kv in sys.argv[3:]:
    k,v = kv.split(":")
    formulae[k] = float(v)

handler = EmperSQL(sys.argv[1])

query = "SELECT node FROM population"
nodes = handler.select_many(query)

for nodename in nodes:
    pnum = handler.calc_points(nodename)
    if pnum == 0:
        print_error("NO NODE: %s (%s)" % (sys.argv[2], nodename[0]))
        raise ValueError("wrong arg")

    mass = 0.0
    for xy in  handler.nodepoints_generator(nodename[0]):
        current = 0.0
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
            current += formulae[color]
        except KeyError: pass
        try:
            if handler.is_coast(*xy):
                current += formulae["COAST"]
        except KeyError: pass
        try:
            i = -(xy[1] - formulae["HLINE"])**2
            f = math.exp(i / formulae["SIGMA"])
            if f < formulae["THOLD"]: current = 0.0
            else: current *= f 
        except KeyError: pass
        mass += current

    value = 0 if mass < 0 else mass/pnum
    args = (sys.argv[2], value, nodename[0])
    handler.execute("UPDATE sources set %s=%g WHERE node='%s'" % args)
    print_out("%s: %g" % (nodename[0], value))
    
del handler
measure_time(start_time)

