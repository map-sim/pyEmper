#! /usr/bin/python3

# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# application: EMPER simulator
# brief: economic and strategic simulator
# opensource licence: GPL-3.0

from time import time
start_time = time() 

import getopt
import sys, os
import sqlite3
from tools import *
from EmperSQL import EmperSQL


if not len(sys.argv) in (3, 4, 5, 6):
    rest = "<database> <outimg> --border=<float> --resize=<int> --median"
    print_error("USAGE: %s %s" % (sys.argv[0], rest))
    raise ValueError("wrong args number")

map_resize = 1
median_flag = False
border_brightness = 0

longopts = ["border=", "resize=", "median"]
opts, args = getopt.getopt(sys.argv[3:], "", longopts)
for opt,arg in opts:
    if opt == "--border":
        border_brightness = float(arg)
        print_info("print borders: %g" % border_brightness)
        
    if opt == "--resize":
        map_resize = int(arg)
        print_info("resize map: %d" % map_resize)
        
    if opt == "--median":
        median_flag = True
        print_info("medianing")

handler = EmperSQL(sys.argv[1])

width = int(handler.get_parameter("width"))
height = int(handler.get_parameter("height"))
print_out("out image: %s" % sys.argv[2])

with open(sys.argv[2], "w") as fd:
    fd.write("P3\n%d %d\n255\n" % (map_resize*width, map_resize*height))
    for color in handler.tmappoints_generator(border_brightness, map_resize):    
        fd.write("%d\n%d\n%d\n" % color)

if median_flag:
    map_medianing(sys.argv[2], map_resize+1)

del handler
measure_time(start_time)
