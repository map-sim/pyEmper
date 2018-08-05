#! /usr/bin/python3

# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# application: EMPER simulator
# brief: economic and strategic simulator
# opensource licence: GPL-3.0

from time import time
start_time = time() 

import json
import getopt
import sys, os
from tools import *

from EmperSQL import EmperSQL
from MapExtracter import MapExtracter

if len(sys.argv) < 6:
    rest = "--palette=<pfile> --resize=<int> --rivers --median <type> <name>"
    print_error("USAGE: %s <database> <outimg> %s" % (sys.argv[0], rest))
    raise ValueError("wrong args number")

config = MapExtracter()
palette = config.parse_palette() 
map_resize = config.parse_resize()
rivers_flag = config.parse_rivers()
median_flag = config.parse_median()

handler = EmperSQL(sys.argv[1])

width = int(handler.get_parameter("width"))
height = int(handler.get_parameter("height"))
print_out("out image: %s" % sys.argv[2])

if "pmap" == sys.argv[-2]:
    try: nation = handler.get_nation_name(sys.argv[-1])
    except ValueError: nation = sys.argv[-1]
    
    distribution = handler.get_nation_distribution(nation)
    maxval = handler.get_nation_maxgroup()

elif "smap" == sys.argv[-2]:
    distribution = handler.get_source_distribution(sys.argv[-1])
    maxval = max(distribution.values())

elif "bmap" == sys.argv[-2]:
    distribution = handler.get_building_distribution(sys.argv[-1])
    maxval = max(distribution.values())

else:
    print_error("type error")
    raise ValueError("type")

    
with open(sys.argv[2], "w") as fd:
    fd.write("P3\n%d %d\n255\n" % (map_resize * width, map_resize * height))
    
    for x, y in xy_gener (width, height, map_resize):

        if handler.is_border(x, y):
            if handler.is_coast(x, y):            
                fd.write("%d\n%d\n%d\n" % tuple(palette["COAST"]))
            else: fd.write("%d\n%d\n%d\n" % tuple(palette["BORDER"]))

        elif rivers_flag and handler.is_river(x, y):
            fd.write("%d\n%d\n%d\n" % tuple(palette["RIVER"]))
            
        elif not handler.is_buildable(x, y):
            if handler.diagram[(x, y)][0] in distribution.keys():
                partpalette = zip(palette["MIN"],palette["MAX"])
                factor = float(distribution[handler.diagram[(x, y)][0]]) / maxval
                color = tuple([int(mo+factor*(me-mo)) for mo,me in partpalette])                
            else:
                color = tuple(palette["OUT2"])            
            fd.write("%d\n%d\n%d\n" % color)
            
        else:
            if handler.diagram[(x, y)][0] in distribution.keys():
                partpalette = zip(palette["MIN"],palette["MAX"])
                factor = float(distribution[handler.diagram[(x, y)][0]]) / maxval
                color = tuple([int(mo+factor*(me-mo)) for mo,me in partpalette])                
            else:
                color = tuple(palette["OUT"])            
            fd.write("%d\n%d\n%d\n" % color)

if median_flag:
    map_medianing(sys.argv[2], 2)
        
del handler
measure_time(start_time)
