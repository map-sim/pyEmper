#! /usr/bin/python3

# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# application: EMPER simulator
# brief: economic and strategic simulator
# opensource licence: GPL-3.0

from time import time
start_time = time() 

import sys
import sqlite3

from tools import print_out
from tools import print_info
from tools import print_error

from EmperSQL import EmperSQL


if len(sys.argv) != 2:
    print_error("USAGE: %s <database>" % sys.argv[0])
    raise ValueError("wrong args number")

def check_table_exists(handler, tablename):
    try:
        handler.execute("SELECT 1 FROM %s" % tablename)
        print_out("%s table exists ... ok" % tablename)
    except sqlite3.OperationalError:
        print_error("%s table does not exist ..." % tablename)

handler = EmperSQL(sys.argv[1])

check_table_exists(handler, "parameters")
check_table_exists(handler, "terrains")
check_table_exists(handler, "nations")
check_table_exists(handler, "nodes")
check_table_exists(handler, "atoms")

atoms_raw = handler.select_many("SELECT * FROM atoms")
height = handler.get_parameter("height")
width = handler.get_parameter("width")
if len(atoms_raw) == height * width and len(atoms_raw) > 0:
    print_out("atoms number (%d) ... ok" % len(atoms_raw))
else: print_error("worng atoms number ...")

terrains_raw = handler.select_many("SELECT * FROM terrains")
terrains_nr = handler.get_parameter("terrains")
if len(terrains_raw) == terrains_nr and terrains_nr > 0:
    print_out("terrains number (%d) ... ok" % terrains_nr)
else: print_error("worng terrains number ...")

nations_raw = handler.select_many("SELECT * FROM nations")
nations_nr = handler.get_parameter("nations")
if len(nations_raw) == nations_nr and nations_nr > 0:
    print_out("nations number (%d) ... ok" % nations_nr)
else: print_error("worng nations number ...")

nodes_raw = handler.select_many("SELECT * FROM nodes")
nodes_nr = handler.get_parameter("nodes")
if len(nodes_raw) == nodes_nr and nodes_nr > 0:
    print_out("nodes number (%d) ... ok" % nodes_nr)
else: print_error("worng nodes number ...")

del handler
stop_time = time()
delta_time = stop_time - start_time     
print_info("duration: %.3f s" % delta_time)
