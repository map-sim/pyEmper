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
from tools import print_info
from tools import print_error

from EmperSQL import EmperSQL


if len(sys.argv) != 5:
    print_error("USAGE: %s <database> <start> <proxy> <stop>" % sys.argv[0])
    raise ValueError("wrong args number")
else:
    handler = EmperSQL(sys.argv[1])
    
handler.enable_diagram()
scale =  handler.get_parameter("scale")

try: startname = handler.get_nodename(int(sys.argv[2]))
except ValueError: startname = sys.argv[2]    

try: proxyname = handler.get_nodename(int(sys.argv[3]))
except ValueError: proxyname = sys.argv[3]    

try: stopname = handler.get_nodename(int(sys.argv[4]))
except ValueError: stopname = sys.argv[4]    

terrdict = handler.get_terrdict()
# print(handler.diagram)
# print(terrdict)

s = "%s -> %s -> %s" % (startname, proxyname, stopname)
print_info(s)

startpoints = []
g = handler.xynode_generator(startname)
for x,y in g:    
    for dx,dy in [(0,1), (0,-1), (1,0), (-1,0)]:
        try:
            if handler.is_node(x+dx, y+dy, proxyname):
                startpoints.append((x+dx, y+dy))
        except KeyError: continue

print_info("starting points: %d" % len(startpoints))

del handler
stop_time = time()
delta_time = stop_time - start_time     
print_info("duration: %.3f s" % delta_time)
