#! /usr/bin/python3

# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# application: EMPER simulator
# brief: economic and strategic simulator
# opensource licence: GPL-3.0

from time import time
start_time = time() 

import sys
import sqlite3

from tools import print_out
from tools import print_info
from tools import print_error

from EmperSQL import EmperSQL


if len(sys.argv) != 2:
    print_error("USAGE: %s <database>" % sys.argv[0])
    raise ValueError("wrong args number")


handler = EmperSQL(sys.argv[1])

query = "SELECT name FROM population"
nodes = handler.select_many(query)


for nodename in nodes:
    pnumber = handler.calc_points(nodename)
    if pnumber == 0:
        print_error("NO NODE: %s (%s)" % (sys.argv[2], nodename))
        raise ValueError("wrong arg")

    query = "SELECT x,y FROM atoms WHERE node='%s'" % nodename
    point = handler.select_row(query)
    checked_points = set([point])
    active_points = set([point])

    while active_points:
        try: x,y = active_points.pop()
        except KeyError: break
    
        for dx,dy in [(0,1), (0,-1), (1,0), (-1,0)]:
            try:
                if handler.is_node(x+dx, y+dy, nodename[0]):
                    if (x+dx, y+dy) in checked_points:
                        continue
                    else:
                        active_points.add((x+dx, y+dy))
                        checked_points.add((x+dx, y+dy))
            except KeyError: continue

    if len(checked_points) != pnumber:
        args = (nodename[0],  pnumber, len(checked_points))
        print_out("%s node is not continuous (%d != %d)" % args)

del handler
stop_time = time()
delta_time = stop_time - start_time     
print_info("duration: %.3f s" % delta_time)
