#! /usr/bin/python3

# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# application: EMPER simulator
# brief: economic and strategic simulator
# opensource licence: GPL-3.0


import sys, os
import sqlite3

from tools import str_to_rgb
from tools import get_parameter
from termcolor import colored

if not os.path.exists(sys.argv[1]):
    error = colored("(error)", "red")
    print(error, "path %s not exists!" % sys.argv[1])
    raise ValueError("database not exists")

conn = sqlite3.connect(sys.argv[1])
print(colored("database:", "green"), sys.argv[1])
cur = conn.cursor()

width = int(get_parameter(cur, "width"))
height = int(get_parameter(cur, "height"))
print(colored("size:", "green"), width, height)

query = "SELECT x,y,color FROM atoms"
cur.execute(query)
xyterr = {}

for x,y,c in cur.fetchall():
    xyterr[(x,y)] = c

with open(sys.argv[2], "w") as fd:
    fd.write("P3\n%d %d\n255\n" % (width, height))
    for y in range(height):
        for x in range(width):
            fd.write("%d\n%d\n%d\n" % str_to_rgb(xyterr[(x,y)]))

print(colored("output:", "green"), sys.argv[2])
conn.close()


