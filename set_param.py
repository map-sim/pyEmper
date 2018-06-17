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


if len(sys.argv) != 4:
    print_error("USAGE: %s <database> <param> <value>" % sys.argv[0])
    raise ValueError("wrong args number")

handler = EmperSQL(sys.argv[1])

query = "SELECT * FROM parameters WHERE name='%s'" % sys.argv[2]
exists = len(handler.select_many(query))

if exists > 0:
    query = "UPDATE parameters SET value=%g WHERE name='%s'" % (float(sys.argv[3]), sys.argv[2])
else:
    query = "INSERT INTO parameters VALUES('%s', %g)" % (sys.argv[2], float(sys.argv[3]))

handler.execute(query)
handler.commit()

val = handler.get_parameter(sys.argv[2])
print_out("%s: %g" % (sys.argv[2], val))

del handler
measure_time(start_time)
