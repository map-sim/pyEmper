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

check_table_exists(handler, "atoms")
check_table_exists(handler, "nations")
check_table_exists(handler, "terrains")
check_table_exists(handler, "parameters")
check_table_exists(handler, "population")
check_table_exists(handler, "resources")
check_table_exists(handler, "building")
check_table_exists(handler, "sources")

width = handler.get_parameter("width")
height = handler.get_parameter("height")
atoms_raw = handler.select_many("SELECT * FROM atoms")
if len(atoms_raw) == height * width and len(atoms_raw) > 0:
    print_out("atoms number (%d) ... ok" % len(atoms_raw))
else: print_error("worng atoms number ...")

terrains_nr = handler.get_parameter("terrains")
terrains_raw = handler.select_many("SELECT * FROM terrains")
if len(terrains_raw) == terrains_nr and terrains_nr > 0:
    print_out("terrains number (%d) ... ok" % terrains_nr)
else: print_error("worng terrains number ...")

resources_nr = handler.get_parameter("resources")
resources_raw = handler.select_many("SELECT * FROM resources")
if len(resources_raw) == resources_nr and resources_nr > 0:
    print_out("resources rows (%d) ... ok" % resources_nr)
else: print_error("worng resources number in population...")

nations_nr = handler.get_parameter("nations")
nations_raw = handler.select_many("SELECT * FROM nations")
if len(nations_raw) == nations_nr and nations_nr > 0:
    print_out("nations number (%d) ... ok" % nations_nr)
else: print_error("worng nations number ...")

nodes_nr = handler.get_parameter("nodes")
sources_raw = handler.select_many("SELECT * FROM sources")
if len(sources_raw) == nodes_nr and nodes_nr > 0:
    print_out("sources rows (%d) ... ok" % nodes_nr)
else: print_error("worng nodes number in sources...")

building_raw = handler.select_many("SELECT * FROM building")
if len(building_raw) == nodes_nr:
    print_out("building rows (%d) ... ok" % nodes_nr)
else: print_error("worng nodes number in building...")

population_raw = handler.select_many("SELECT * FROM population")
if len(population_raw) == nodes_nr:
    print_out("population rows (%d) ... ok" % nodes_nr)
else: print_error("worng nodes number in population...")


del handler
stop_time = time()
delta_time = stop_time - start_time     
print_info("duration: %.3f s" % delta_time)
