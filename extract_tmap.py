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

from tools import print_out
from tools import print_info
from tools import print_error
from tools import str_to_rgb
from tools import xy_gener

from EmperSQL import EmperSQL


if not len(sys.argv) in (3, 4, 5):
    rest = "<database> <outimg> --border=<float> --resize=<int>"
    print_error("USAGE: %s %s" % (sys.argv[0], rest))
    raise ValueError("wrong args number")

map_resize = 1
border_brightness = 1.0
longopts = ["border=", "resize="]
opts, args = getopt.getopt(sys.argv[3:], "", longopts)
for opt,arg in opts:
    if opt == "--border":
        border_brightness = float(arg)
        print_info("print borders: %g" % border_brightness)
    if opt == "--resize":
        map_resize = int(arg)
        print_info("resize map: %d" % map_resize)

handler = EmperSQL(sys.argv[1])

width = int(handler.get_parameter("width"))
height = int(handler.get_parameter("height"))
print_out("out image: %s" % sys.argv[2])

with open(sys.argv[2], "w") as fd:
    fd.write("P3\n%d %d\n255\n" % (map_resize*width, map_resize*height))
    for color in handler.tmappoints_generator(border_brightness, map_resize):    
        fd.write("%d\n%d\n%d\n" % color)

del handler
stop_time = time()
delta_time = stop_time - start_time     
print_info("duration: %.3f s" % delta_time)
