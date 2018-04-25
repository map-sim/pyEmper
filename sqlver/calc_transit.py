#! /usr/bin/python3

# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# application: EMPER simulator
# brief: economic and strategic simulator
# opensource licence: GPL-3.0


import sys, os
import sqlite3
from tools import print_info
from tools import print_error

from EmperSQL import EmperSQL


if len(sys.argv) != 5:
    print_error("USAGE: %s <database> <start> <proxy> <stop>" % sys.argv[0])
    raise ValueError("wrong args number")
else:
    handler = EmperSQL(sys.argv[1])
    
handler.enable_diagram()
scale =  handler.get_parameter("scale")

try:
    startname = handler.get_node_name(int(sys.argv[2]))
except ValueError: startname = sys.argv[2]    

try:
    proxyname = handler.get_node_name(int(sys.argv[3]))
except ValueError: proxyname = sys.argv[3]    

try:
    stopname = handler.get_node_name(int(sys.argv[4]))
except ValueError: stopname = sys.argv[4]    

print(startname, proxyname, stopname)
