#! /usr/bin/python3

# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# application: EMPER simulator
# brief: economic and strategic simulator
# opensource licence: GPL-3.0


import sys, os
import sqlite3

from tools import str_to_rgb
from tools import print_info
from tools import print_error
from tools import xy_gener

from EmperSQL import EmperSQL


if len(sys.argv) != 3:
    print_error("USAGE: %s <database> <node>" % sys.argv[0])
    raise ValueError("wrong args number")
else:
    handler = EmperSQL(sys.argv[1])
    handler.enable_diagram()

width = int(handler.get_parameter("width"))
height = int(handler.get_parameter("height"))
print_info("size: %d x %d" % (width, height))

try:
    nodename = handler.get_node_name(int(sys.argv[2]))
except ValueError:
    nodename = sys.argv[2]    
noderow = handler.select_node(nodename)
points = handler.select_points(noderow[0])
scale =  handler.get_parameter("scale")

print("name:", noderow[0])    
print("atoms:", len(points))
print("area:", scale * len(points))
