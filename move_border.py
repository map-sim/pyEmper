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
from tools import *
from EmperSQL import EmperSQL


if not len(sys.argv) in (4, 6):
    print_error("USAGE: %s <database> <node1> <node2> <int> <int>" % sys.argv[0])
    raise ValueError("wrong args number")

handler = EmperSQL(sys.argv[1])

xlimit = 0
ylimit = 0
if len(sys.argv) == 6:
    xlimit = int(sys.argv[4])
    ylimit = int(sys.argv[5])
    print_info("limit: %d %d" % (xlimit, ylimit))

try: startname = handler.get_node_name(int(sys.argv[2]))
except ValueError: startname = sys.argv[2]    

try: stopname = handler.get_node_name(int(sys.argv[3]))
except ValueError: stopname = sys.argv[3]    

counter = 0
points = handler.get_common_points(stopname, startname)
for x,y in points:
    
    if xlimit < 0:
        if x > -xlimit:
            continue
    elif  xlimit > 0:
        if x < xlimit:
            continue
        
    if ylimit > 0:
        if y > ylimit:
            continue
    elif  ylimit < 0:
        if y < -ylimit:
            continue

    counter += 1
    query = "UPDATE atoms SET node='%s' WHERE x=%d AND y=%d" % (startname, x, y)
    handler.execute(query)
                 
print_out("moved: %d / %d" % (counter, len(points)))

del handler
measure_time(start_time)
