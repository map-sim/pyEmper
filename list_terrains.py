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
terrs = handler.select_many("SELECT * FROM terrains")
for t in terrs:
    print_out("%s\t(%s):\t%g\t%g\t%g\t%g" % t)

del handler
stop_time = time()
delta_time = stop_time - start_time     
print_info("duration: %.3f s" % delta_time)
