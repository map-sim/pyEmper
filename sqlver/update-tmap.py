#! /usr/bin/python3

# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# application: EMPER simulator
# brief: economic and strategic simulator
# opensource licence: GPL-3.0


import sys, os
import sqlite3

from tools import str_to_rgb
from tools import ppm_loader
from tools import get_parameter
from tools import get_nearest_rgb
from termcolor import colored

if not os.path.exists(sys.argv[1]):
    error = colored("(error)", "red")
    print(error, "path %s not exists!" % sys.argv[1])
    raise ValueError("database not exists")

if not os.path.exists(sys.argv[2]):
    error = colored("(error)", "red")
    print(error, "path %s not exists!" % sys.argv[2])
    raise ValueError("mapfile not exists")

conn = sqlite3.connect(sys.argv[1])
print(colored("database:", "green"), sys.argv[1])
print(colored("input:", "green"), sys.argv[2])
cur = conn.cursor()

width = int(get_parameter(cur, "width"))
height = int(get_parameter(cur, "height"))
print(colored("size:", "green"), width, height)

m_width, m_height, generator = ppm_loader(sys.argv[2])
if int(m_width) < 0 or width != m_width: raise  ValueError("width is wrong")
if int(m_height) < 0 or height != m_height: raise  ValueError("height is wrong")

query = "SELECT color FROM terrains"
cur.execute(query)

hist = {}
conv = {}
for c in cur.fetchall():
    rgb = str_to_rgb(c[0])
    conv[rgb] = c[0]
    hist[rgb] = 0
print(colored("terrains:", "green"), len(hist))

buffer = {}
query = "SELECT * FROM atoms"
cur.execute(query)
for raw in cur.fetchall():
    buffer[(raw[0], raw[1])] = [raw[2], raw[3]]
    
for n, rgb in generator:    
    try:
        hist[rgb] += 1
    except KeyError:
        rgb = get_nearest_rgb(tuple(hist.keys()), rgb)
        print("warning:", [hex(c) for c in rgb]) 

    x = n % width
    y = n // width
    buffer[(x, y)][1] = conv[rgb]

query = "DELETE FROM atoms"
cur.execute(query)


for xy in buffer.keys():

    query = "INSERT INTO atoms VALUES (%d, %d, '%s', '%s')" % (xy[0], xy[1], buffer[xy][0], buffer[xy][1])
    cur.execute(query)

conn.commit()
conn.close()


