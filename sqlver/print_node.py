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

from tools import print_info
from tools import print_error

from EmperSQL import EmperSQL


if len(sys.argv) != 3:
    print_error("USAGE: %s <database> <node>" % sys.argv[0])
    raise ValueError("wrong args number")
else:
    handler = EmperSQL(sys.argv[1])
handler.enable_diagram()

try: nodename = handler.get_nodename(int(sys.argv[2]))
except ValueError: nodename = sys.argv[2]    

scale =  handler.get_parameter("scale")
pnumber = handler.calc_points(nodename)
if pnumber == 0:
    print_error("NO NODE: %s (%s)" % (sys.argv[2], nodename))
    raise ValueError("wrong arg")

print("name:", nodename)    
print("atoms:", pnumber)
print("area: %g" % (scale * pnumber))

buffer = {}
g = handler.xynode_generator(nodename)
for x,y in g:    
    for dx,dy in [(0,1), (0,-1), (1,0), (-1,0)]:
        try:
            if handler.is_node(x+dx, y+dy, nodename):
                continue
            othernode = handler.diagram[(x+dx, y+dy)][0]
        except KeyError: continue
        try: buffer[othernode] += 1
        except KeyError: buffer[othernode] = 1

print("borders:")
for name in buffer.keys():
    print("\t%s: %d" % (name, buffer[name]))

del handler
stop_time = time()
delta_time = stop_time - start_time     
print_info("duration: %.3f s" % delta_time)
