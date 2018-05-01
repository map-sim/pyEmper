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
import getopt
import json

from tools import print_out
from tools import print_info
from tools import print_error
from tools import str_to_rgb
from tools import xy_gener

from EmperSQL import EmperSQL


if len(sys.argv) < 4:
    rest = "--palette=<pfile> --resize=<int> <node1> <node2:color1> ..."
    print_error("USAGE: %s <database> <outimg> %s" % (sys.argv[0], rest))
    raise ValueError("wrong args number")

map_resize = 1
longopts = ["palette=", "resize="]
opts, args = getopt.getopt(sys.argv[3:], "", longopts)
for opt,arg in opts:
    if opt == "--palette":
        if not os.path.exists(arg):
            print_error("PALETTE does not exist: %s" % arg)
            raise ValueError("wrong arg value")
            
        print_info("palette: %s" % arg)
        with open(arg) as f:
            palette = json.load(f)
    if opt == "--resize":
        map_resize = int(arg)
        print_info("resize map: %d" % map_resize)
        
handler = EmperSQL(sys.argv[1])
handler.enable_diagram()

nodes = []
combos = {}
for node in args:
    try:
        nodename, color = node.split(":")
        combos[nodename] = str_to_rgb(color)
    except ValueError: 
        try: nodename = handler.get_nodename(int(node))
        except ValueError: nodename = node    
        nodes.append(nodename)

width = int(handler.get_parameter("width"))
height = int(handler.get_parameter("height"))
print_out("out image: %s" % sys.argv[2])

with open(sys.argv[2], "w") as fd:
    fd.write("P3\n%d %d\n255\n" % (map_resize * width, map_resize * height))
    
    for x, y in xy_gener (width, height, map_resize):
        if handler.is_border(x, y):
            fd.write("%d\n%d\n%d\n" % tuple(palette["BORDERS"]))

        elif handler.diagram[(x,y)][0] in combos.keys():
            fd.write("%d\n%d\n%d\n" % combos[handler.diagram[(x,y)][0]])

        elif [True for node in nodes if handler.is_node(x, y, node)]:
            if handler.is_buildable(x, y):
                fd.write("%d\n%d\n%d\n" % tuple(palette["MARKED-LANDS"]))
            else: fd.write("%d\n%d\n%d\n" % tuple(palette["MARKED-WATERS"]))
        
        else: 
            if handler.is_buildable(x, y):
                fd.write("%d\n%d\n%d\n" % tuple(palette["LANDS"]))
            else: fd.write("%d\n%d\n%d\n" % tuple(palette["WATERS"]))        

del handler
stop_time = time()
delta_time = stop_time - start_time     
print_info("duration: %.3f s" % delta_time)

