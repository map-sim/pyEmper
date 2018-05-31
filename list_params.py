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
from tools import *
from EmperSQL import EmperSQL


if len(sys.argv) != 2:
    print_error("USAGE: %s <database>" % sys.argv[0])
    raise ValueError("wrong args number")

handler = EmperSQL(sys.argv[1])
params = handler.select_many("SELECT * FROM parameters")
for p in params: print_out("%s: %g" % (p[0], p[1]))

del handler
measure_time(start_time)
