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

resources = handler.select_many("SELECT * FROM resources")
resources_nr = handler.get_parameter("resources")
print_info("resources: %d" % resources_nr)

if len(resources) != resources_nr:
    print_error("%d resources registred!" % len(resources))
    raise ValueError("resources number not correct")

sources = handler.get_table_columns("sources")
for r in resources:
    if r[0] in sources:
        print_out("%s\t[*]" % r[0])
    else:
        print_out("%s\t[ ]" % r[0])

del handler
measure_time(start_time)

