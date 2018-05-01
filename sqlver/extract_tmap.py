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

from tools import str_to_rgb
from tools import print_info
from tools import print_error
from tools import xy_gener

from EmperSQL import EmperSQL


if not len(sys.argv) in (2, 3, 4):
    print_error("USAGE: %s <database> --border=<float> --resize=<int>" % sys.argv[0])
    raise ValueError("wrong args number")

map_resize = 1
border_brightness = 1.0
longopts = ["border=", "resize="]
opts, args = getopt.getopt(sys.argv[2:], "", longopts)
for opt,arg in opts:
    if opt == "--border":
        border_brightness = float(arg)
        print_info("print borders: %g" % border_brightness)
    if opt == "--resize":
        map_resize = int(arg)
        print_info("resize map: %d" % map_resize)

handler = EmperSQL(sys.argv[1])
handler.enable_diagram()

xyterr = {}
query = "SELECT x,y,color FROM atoms"
for x,y,c in handler.select_many(query):
    xyterr[(x,y)] = c

width = int(handler.get_parameter("width"))
height = int(handler.get_parameter("height"))
sys.stdout.write("P3\n%d %d\n255\n" % (map_resize*width, map_resize*height))

for x, y in xy_gener (width, height, map_resize):
    if handler.is_border(x, y):
        rgb = tuple([int(border_brightness * c) for c in str_to_rgb(xyterr[(x,y)])])
        sys.stdout.write("%d\n%d\n%d\n" % rgb)
    else:
        sys.stdout.write("%d\n%d\n%d\n" % str_to_rgb(xyterr[(x,y)]))

del handler
stop_time = time()
delta_time = stop_time - start_time     
print_info("duration: %.3f s" % delta_time)
