#! /usr/bin/python3

# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# application: EMPER simulator
# brief: economic and strategic simulator
# opensource licence: GPL-3.0


import sys, os
import sqlite3

from termcolor import colored

if not os.path.exists(sys.argv[1]):
    error = colored("(error)", "red")
    print(error, "path %s not exists!" % sys.argv[1])


def get_parameter(cur, name):
    query = "SELECT value FROM parameters WHERE name='%s'" % name 
    cur.execute(query)
    return cur.fetchone()[0]

def str2rgb(strrgb):
    r = int(strrgb[0:2], 16)
    g = int(strrgb[2:4], 16)
    b = int(strrgb[4:], 16)
    return r, g, b
    
conn = sqlite3.connect(sys.argv[1])
cur = conn.cursor()

width = int(get_parameter(cur, "width"))
height = int(get_parameter(cur, "height"))
print("size:", width, height)

query = "SELECT color FROM terrains"
cur.execute(query)
pallete = [str2rgb(c[0]) for c in cur.fetchall()]

query = "SELECT x,y,terrain FROM atoms"
cur.execute(query)
xyt = {}

for x,y,t in cur.fetchall():
    xyt[(x,y)] = t

with open(sys.argv[2], "w") as fd:
    fd.write("# author: Krzysztof Czarnecki\n")
    fd.write("# email: czarnecki.krzysiek@gmail.com\n")
    fd.write("# application: EMPER simulator\n")
    fd.write("# brief: economic and strategic simulator\n")
    fd.write("# opensource licence: GPL-3.0\n")
    fd.write("P3\n")
    fd.write("%d %d\n" % (width, height))
    fd.write("255\n")

    for y in range(height):
        for x in range(width):
            fd.write("%d\n%d\n%d\n" % pallete[xyt[(x,y)]])

conn.close()

