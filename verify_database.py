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
from tools import *
from EmperSQL import EmperSQL

if len(sys.argv) != 2:
    print_error("USAGE: %s <database>" % sys.argv[0])
    raise ValueError("wrong args number")


handler = EmperSQL(sys.argv[1])

handler.check_table_exists("atoms")
handler.check_table_exists("nations")
handler.check_table_exists("terrains")
handler.check_table_exists("parameters")
handler.check_table_exists("population")
handler.check_table_exists("processes")
handler.check_table_exists("resources")
handler.check_table_exists("skilling")
handler.check_table_exists("building")
handler.check_table_exists("sources")
handler.check_table_exists("stock")


handler.check_table_has_columns("nations", ["name"])
handler.check_table_has_columns("sources", ["node"])
handler.check_table_has_columns("parameters", ["name", "value"])
handler.check_table_has_columns("atoms", ["x", "y", "node", "color"])
handler.check_table_has_columns("resources", ["name", "toll", "decay"])
handler.check_table_has_columns("terrains", ["name", "color", "base", "ship", "build", "cost"])

nations = handler.get_column("nations", "name")
resources = handler.get_column("resources", "name")
processes = handler.get_column("processes", "name")

handler.check_table_has_columns("stock", ["node", *resources])
handler.check_table_has_columns("population", ["node", *nations])
handler.check_table_has_columns("processes", ["name", "LIVING", "BUILDING", "ENERGY", *resources])

handler.check_table_has_columns("skilling", ["node", *processes])
handler.check_table_has_columns("building", ["node", *processes])


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

nations_nr = handler.get_parameter("nations")
nations_raw = handler.select_many("SELECT * FROM nations")
if len(nations_raw) == nations_nr and nations_nr > 0:
    print_out("nations number (%d) ... ok" % nations_nr)
else: print_error("worng nations number ...")

resources_nr = handler.get_parameter("resources")
resources_raw = handler.select_many("SELECT * FROM resources")
if len(resources_raw) == resources_nr and resources_nr > 0:
    print_out("resources rows (%d) ... ok" % resources_nr)
else: print_error("worng resources number...")

processes_nr = handler.get_parameter("processes")
processes_raw = handler.select_many("SELECT * FROM processes")
if len(processes_raw) == processes_nr and processes_nr > 0:
    print_out("processes rows (%d) ... ok" % processes_nr)
else: print_error("worng processes number...")

sources_nr = handler.get_parameter("sources")
sources_raw = handler.select_many("SELECT * FROM sources")
if len(sources_raw[0]) - 1 == sources_nr and \
   resources_nr >= sources_nr > 0:
    print_out("sources rows (%d) ... ok" % sources_nr)
else: print_error("worng sources number...")

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

stock_raw = handler.select_many("SELECT * FROM stock")
if len(stock_raw) == nodes_nr:
    print_out("stock rows (%d) ... ok" % nodes_nr)
else: print_error("worng nodes number in stock...")


del handler
measure_time(start_time)
