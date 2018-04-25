#! /usr/bin/python3

# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# application: EMPER simulator
# brief: economic and strategic simulator
# opensource licence: GPL-3.0


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

width = int(handler.get_parameter("width"))
height = int(handler.get_parameter("height"))
print_info("size: %d x %d" % (width, height))

try:
    nodename = handler.get_node_name(int(sys.argv[2]))
except ValueError: nodename = sys.argv[2]    

scale =  handler.get_parameter("scale")
points = handler.select_points(nodename)
if len(points) == 0:
    print_error("NO NODE: %s" % sys.argv[2])
    raise ValueError("wrong arg")

print("name:", nodename)    
print("atoms:", len(points))
print("area: %g" % (scale * len(points)))
