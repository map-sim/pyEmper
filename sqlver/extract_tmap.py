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


if not len(sys.argv) in (2, 3):
    print_error("USAGE: %s <database> [-b]" % sys.argv[0])
    raise ValueError("wrong args number")
else:
    handler = EmperSQL(sys.argv[1])

if "-b" in sys.argv:
    print_info("print borders")
    handler.enable_diagram()

width = int(handler.get_parameter("width"))
height = int(handler.get_parameter("height"))
print_info("size: %d x %d" % (width, height))

xyterr = {}
query = "SELECT x,y,color FROM atoms"
for x,y,c in handler.select_many(query):
    xyterr[(x,y)] = c

sys.stdout.write("P3\n%d %d\n255\n" % (width, height))
if "-b" in sys.argv:
    for x, y in xy_gener (width, height):
        if handler.is_border(x, y): sys.stdout.write("%d\n%d\n%d\n" % (255, 255, 255))
        else: sys.stdout.write("%d\n%d\n%d\n" % str_to_rgb(xyterr[(x,y)]))
else:
    for x, y in xy_gener (width, height):
        sys.stdout.write("%d\n%d\n%d\n" % str_to_rgb(xyterr[(x,y)]))



