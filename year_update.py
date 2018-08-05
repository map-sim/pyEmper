#! /usr/bin/python3

# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# application: EMPER simulator
# brief: economic and strategic simulator
# opensource licence: GPL-3.0

from time import time
start_time = time() 

import re
import sys, os
from tools import *
from EmperSQL import EmperSQL

if len(sys.argv) < 2:
    print_error("USAGE: %s <database>" % sys.argv[0])
    raise ValueError("wrong args number")

handler = EmperSQL(sys.argv[1])

query = "SELECT * FROM population"
nod_population = handler.select_many(query)

query = "SELECT * FROM processes"
process_list = handler.select_many(query)

scale = handler.get_parameter("scale")
fertility = handler.get_parameter("fertility")
performance = handler.get_parameter("performance")
productivity = handler.get_parameter("productivity")

for node_line in nod_population:
    nodename = node_line[0]
    # print_info("node: {}".format(nodename))
    
    people = sum(node_line[1:])
    # print_info("people: {}".format(people))

    query = "SELECT * FROM building WHERE node='{}'".format(nodename)
    building_line = handler.select_many(query)[1:]

    bsum = sum(building_line)
    # print_info("buildngs: {}".format(bsum))
    
    bfactor = performance * bsum   
    # print_info("bfactor: {}".format(bfactor))
    
    area = handler.calc_points(nodename)
    
    afactor = fertility * area
    # print_info("afactor: {}".format(afactor))
    
    for p in process_list:
        if not re.search("\A_source", p[0]):
            continue

        args = p[0], node_line[0]
        query = "SELECT {} FROM building WHERE node='{}'".format(*args)
        buildings = handler.select_many(query)[0][0]
        xfactor = performance * buildings
        
        srcname = p[0].split("_")[-1].upper()
        args = srcname, node_line[0]
        query = "SELECT {} FROM sources WHERE node='{}'".format(*args)
        source = handler.select_many(query)[0][0]

        pfactor = people * (xfactor + afactor) / (bfactor + afactor) 
        good = pfactor * source 

        out = "* {} -> {}".format(p[0], good)
        print_info(out)
    
    for p in process_list:
        if not re.search("\Aenergy", p[0]):
            continue
    
        # print("*", p[0])
    
    for p in process_list:
        if re.search("\Aenergy", p[0]):
            continue
        if re.search("\A_source", p[0]):
            continue
        if re.search("\A_living", p[0]):
            continue
        if re.search("\A_building", p[0]):
            continue
    
        # print("*", p[0])

    for p in process_list:
        if not re.search("\A_building", p[0]):
            continue
    
        # print("*", p[0])
    
del handler
measure_time(start_time)
