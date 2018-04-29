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
    print_error("USAGE: %s <database> [-b]" % sys.argv[0])
    raise ValueError("wrong args number")

brightness = 1.0
longopts = ["border=", "brightness="]
opts, args = getopt.getopt(sys.argv[2:], "", longopts)
for opt,arg in opts:
    if opt == "--border":
        print_info("print borders")
        border_color = str_to_rgb(arg)
    if opt == "--brightness":
        brightness = float(arg)

handler = EmperSQL(sys.argv[1])
handler.enable_diagram()

xyterr = {}
query = "SELECT x,y,color FROM atoms"
for x,y,c in handler.select_many(query):
    xyterr[(x,y)] = c

width = int(handler.get_parameter("width"))
height = int(handler.get_parameter("height"))
sys.stdout.write("P3\n%d %d\n255\n" % (width, height))

if "border_color" in vars():
    for x, y in xy_gener (width, height):
        if handler.is_border(x, y): sys.stdout.write("%d\n%d\n%d\n" % border_color)
        else:
            rgb = tuple([int(brightness * c) for c in str_to_rgb(xyterr[(x,y)])])
            sys.stdout.write("%d\n%d\n%d\n" % rgb)
else:
    for x, y in xy_gener (width, height):
        sys.stdout.write("%d\n%d\n%d\n" % str_to_rgb(xyterr[(x,y)]))

del handler
stop_time = time()
delta_time = stop_time - start_time     
print_info("duration: %.3f s" % delta_time)
