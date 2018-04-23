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

from EmperSQL import EmperSQL


if len(sys.argv) != 2:
    print_error("USAGE: %s <database>" % sys.argv[0])
    raise ValueError("wrong args number")
else:
    handler = EmperSQL(sys.argv[1])

width = int(handler.get_parameter("width"))
height = int(handler.get_parameter("height"))
print_info("size: %d x %d" % (width, height))

xyterr = {}
query = "SELECT x,y,node FROM atoms"
for x,y,n in handler.select_many(query):
    xyterr[(x,y)] = n

border_color = (0, 0, 0)
noborder_color = (255, 255, 255)

sys.stdout.write("P3\n%d %d\n255\n" % (width, height))
for y in range(height):
    for x in range(width):
        border = False

        try:
            if xyterr[(x,y)] != xyterr[(x+1,y)]:
                border = True
        except KeyError: pass
        try:
            if xyterr[(x,y)] != xyterr[(x-1,y)]:
                border = True
        except KeyError: pass
        try:
            if xyterr[(x,y)] != xyterr[(x,y+1)]:
                border = True
        except KeyError: pass
        try:
            if xyterr[(x,y)] != xyterr[(x,y-1)]:
                border = True
        except KeyError: pass
        
        if border: sys.stdout.write("%d\n%d\n%d\n" % border_color)
        else: sys.stdout.write("%d\n%d\n%d\n" % noborder_color)


