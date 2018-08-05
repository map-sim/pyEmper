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


if len(sys.argv) < 3:
    print_error("USAGE: %s <database> <build>" % sys.argv[0])
    raise ValueError("wrong args number")

formulae = {}
for kv in sys.argv[3:]:
    k,v = kv.split(":")
    formulae[k] = float(v)

handler = EmperSQL(sys.argv[1])

query = "SELECT node FROM building"
nodes = handler.select_many(query)

for nodename in nodes:
    pnum = handler.calc_points(nodename)
    if pnum == 0:
        print_error("NO NODE: %s (%s)" % (sys.argv[2], nodename[0]))
        raise ValueError("wrong arg")

    value = 0

    args = (sys.argv[2], value, nodename[0])
    handler.execute("UPDATE building set %s=%g WHERE node='%s'" % args)
    print_out("%s: %g" % (nodename[0], value))
    
del handler
measure_time(start_time)
