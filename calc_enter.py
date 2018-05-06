#! /usr/bin/python3

# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# application: EMPER simulator
# brief: economic and strategic simulator
# opensource licence: GPL-3.0

from time import time
start_time = time() 

import sys, os
import sqlite3, math
from tools import print_out
from tools import print_info
from tools import print_error

from EmperSQL import EmperSQL


if len(sys.argv) < 4:
    print_error("USAGE: %s <database> <start> <start> ... <stop>" % sys.argv[0])
    raise ValueError("wrong args number")

handler = EmperSQL(sys.argv[1])    
startnodes = set()

for nodename in sys.argv[2:-1]:

    try: nodename = handler.get_node_name(int(nodename))
    except ValueError: nodename = nodename
    startnodes.add(nodename)

try: stopname = handler.get_node_name(int(sys.argv[-1]))
except ValueError: stopname = sys.argv[-1]

if stopname in startnodes:
    print_error("stop node in enter nodes!")
    raise ValueError("wrong call")

enter_cost = handler.calc_enter(startnodes, stopname)
print_out("enter cost: %g" % enter_cost)

del handler
stop_time = time()
delta_time = stop_time - start_time     
print_info("duration: %.3f s" % delta_time)
