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

from tools import str_to_rgb
from tools import print_info
from tools import print_error
from tools import xy_gener

from EmperSQL import EmperSQL


if len(sys.argv) < 3:
    print_error("USAGE: %s <database> <node1> ... <nodeN>" % sys.argv[0])
    raise ValueError("wrong args number")
else:
    handler = EmperSQL(sys.argv[1])
handler.enable_diagram()
        
width = int(handler.get_parameter("width"))
height = int(handler.get_parameter("height"))
sys.stdout.write("P3\n%d %d\n255\n" % (width, height))

nodes = []
for node in sys.argv[2:]:
    try: nodename = handler.get_nodename(int(node))
    except ValueError: nodename = node    
    nodes.append(nodename)
    
for x, y in xy_gener (width, height):
    if handler.is_border(x, y):
        sys.stdout.write("%d\n%d\n%d\n" % (0, 0, 0))

    elif [True for node in nodes if handler.is_node(x, y, node)]:
        if handler.is_buildable(x, y):
            sys.stdout.write("%d\n%d\n%d\n" % (255, 0, 0))
        else: sys.stdout.write("%d\n%d\n%d\n" % (0, 0, 255))
        
    else: 
        if handler.is_buildable(x, y):
            sys.stdout.write("%d\n%d\n%d\n" % (255, 200, 200))
        else: sys.stdout.write("%d\n%d\n%d\n" % (200, 200, 255))        

del handler
stop_time = time()
delta_time = stop_time - start_time     
print_info("duration: %.3f s" % delta_time)

