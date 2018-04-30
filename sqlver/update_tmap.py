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

from tools import print_info
from tools import print_error

from tools import ppm_loader
from tools import str_to_rgb
from tools import get_nearest_rgb

from EmperSQL import EmperSQL


if len(sys.argv) != 3:
    print_error("USAGE: %s <database> <tmap>" % sys.argv[0])
    raise ValueError("wrong args number")

if not os.path.exists(sys.argv[2]):
    print_error("path %s not exists!" % sys.argv[2])
    raise ValueError("tmap file not exists")
else:
    print_info("tmap input: %s" % sys.argv[2])

handler = EmperSQL(sys.argv[1])
width = int(handler.get_parameter("width"))
height = int(handler.get_parameter("height"))

m_width, m_height, generator = ppm_loader(sys.argv[2])
if int(m_width) < 0 or width != m_width:
    print_error("tmap has wrong sizes")
    raise  ValueError("width is wrong")
elif int(m_height) < 0 or height != m_height:
    print_error("tmap has wrong sizes")
    raise  ValueError("height is wrong")


hist = {}
conv = {}
query = "SELECT color FROM terrains"
for c in handler.select_many(query):
    rgb = str_to_rgb(c[0])
    conv[rgb] = c[0]
    hist[rgb] = 0
print_info("terrains: %d" % len(hist))

buffer = {}
query = "SELECT * FROM atoms"
for raw in handler.select_many(query):
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

handler.execute("DELETE FROM atoms")

for xy in buffer.keys():
    query = "INSERT INTO atoms VALUES (%d, %d, '%s', '%s')" % (xy[0], xy[1], buffer[xy][0], buffer[xy][1])
    handler.execute(query)

del handler

stop_time = time()
delta_time = stop_time - start_time     
print_info("duration: %.3f s" % delta_time)

