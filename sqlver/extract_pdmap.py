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
from tools import get_parameter

if not os.path.exists(sys.argv[1]):
    print_error("path %s not exists!" % sys.argv[1])
    raise ValueError("database not exists")

conn = sqlite3.connect(sys.argv[1])
print_info("database: %s" % sys.argv[1])
cur = conn.cursor()

width = int(get_parameter(cur, "width"))
height = int(get_parameter(cur, "height"))
print_info("size: %d x %d" % (width, height))

query = "SELECT * FROM nations"
cur.execute(query)
nations = cur.fetchall()

query = "SELECT * FROM nodes"
cur.execute(query)
nodes = cur.fetchall()

query = "SELECT x,y,node FROM atoms"
cur.execute(query)
xyterr = {}

for x,y,n in cur.fetchall():
    xyterr[(x,y)] = n

border_color = (0, 0, 0)
noborder_color = (255, 255, 255)

sys.stdout.write("P3\n%d %d\n255\n" % (width, height))
for y in range(height):
    for x in range(width):
        border = False

        try:
            if xyterr[(x,y)] != xyterr[(x+1,y)]: border = True
        except KeyError: pass
        try:
            if xyterr[(x,y)] != xyterr[(x-1,y)]: border = True
        except KeyError: pass
        try:
            if xyterr[(x,y)] != xyterr[(x,y+1)]: border = True
        except KeyError: pass
        try:
            if xyterr[(x,y)] != xyterr[(x,y-1)]: border = True
        except KeyError: pass
        
        if border: sys.stdout.write("%d\n%d\n%d\n" % border_color)
        else: sys.stdout.write("%d\n%d\n%d\n" % noborder_color)
                
conn.close()


