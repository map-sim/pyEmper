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

processes = handler.select_many("SELECT * FROM processes")
names = handler.get_table_columns("processes")

print_info("processes number: %s" % len(processes))

# if len(resources) != resources_nr:
#     print_error("%d resources registred!" % len(resources))
#     raise ValueError("resources number not correct")

for proc in processes:
    counter = 0
    for n, p in enumerate(proc):
        arg = names[n], str(p)
        if p is None:
            continue
        elif counter < 2:
            print_out("%s: %s" % arg)
        else:            
            print_out("\t%s: %s" % arg)
        counter+=1
        
del handler
measure_time(start_time)

