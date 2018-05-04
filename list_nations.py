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

from tools import print_out
from tools import print_info
from tools import print_error

from EmperSQL import EmperSQL


if len(sys.argv) != 2:
    print_error("USAGE: %s <database>" % sys.argv[0])
    raise ValueError("wrong args number")


handler = EmperSQL(sys.argv[1])

natffer = handler.select_many("SELECT * FROM nations")
nations = handler.get_parameter("nations")
print_info("nations: %d" % nations)

if len(natffer) != nations:
    print_error("%d nations registred!" % len(natffer))
    raise ValueError("nations number not correct")

for n in natffer:
    query = "SELECT n_%s FROM nodes WHERE n_%s>0" % (n[0], n[0])
    poppernode = handler.select_many(query)
    pop = sum([c[0] for c in poppernode])
    print_out("%s: %d" % (n[0], int(pop)))

del handler
stop_time = time()
delta_time = stop_time - start_time     
print_info("duration: %.3f s" % delta_time)

