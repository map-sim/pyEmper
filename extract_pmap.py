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
    rest = "--palette=<pfile> --resize=<int> --rivers <nation>"
    print_error("USAGE: %s <database> <outimg> %s" % (sys.argv[0], rest))
    raise ValueError("wrong args number")

map_resize = 1
palette = None
rivers_on = False
longopts = ["palette=", "resize=", "rivers"]
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
        
    if opt == "--rivers":
        rivers_on = True
        print_info("rivers: on")

if not palette:
    print_error("palette has to be loaded")
    raise ValueError("palette")

handler = EmperSQL(sys.argv[1])

try: nation = handler.get_nation_name(args[-1])
except ValueError: nation = args[-1]

width = int(handler.get_parameter("width"))
height = int(handler.get_parameter("height"))
print_out("out image: %s" % sys.argv[2])

distrnat = handler.get_nation_distribution(nation)
maxgroup = handler.get_nation_maxgroup()

with open(sys.argv[2], "w") as fd:
    fd.write("P3\n%d %d\n255\n" % (map_resize * width, map_resize * height))
    
    for x, y in xy_gener (width, height, map_resize):

        if handler.is_border(x, y):
            if handler.is_coast(x, y):            
                fd.write("%d\n%d\n%d\n" % tuple(palette["COAST"]))
            else: fd.write("%d\n%d\n%d\n" % tuple(palette["BORDER"]))

        elif rivers_on and handler.is_river(x, y):
            fd.write("%d\n%d\n%d\n" % tuple(palette["RIVER"]))
            
        elif not handler.is_buildable(x, y):
            fd.write("%d\n%d\n%d\n" % tuple(palette["WATER"]))
            
        else:
            if handler.diagram[(x, y)][0] in distrnat.keys():
                partpalette = zip(palette["MIN"],palette["MAX"])
                factor = float(distrnat[handler.diagram[(x, y)][0]]) / maxgroup
                color = tuple([int(mo+factor*(me-mo)) for mo,me in partpalette])                
            else:
                color = tuple(palette["OUT"])            
            fd.write("%d\n%d\n%d\n" % color)

del handler
stop_time = time()
delta_time = stop_time - start_time     
print_info("duration: %.3f s" % delta_time)

