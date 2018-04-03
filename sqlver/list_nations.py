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
from tools import get_parameter

if not os.path.exists(sys.argv[1]):
    print_error("path %s not exists!" % sys.argv[1])
    raise ValueError("database not exists")

conn = sqlite3.connect(sys.argv[1])
print_info("database: %s" % sys.argv[1])
cur = conn.cursor()

query = "SELECT * FROM nations"
cur.execute(query)
natffer = cur.fetchall()

nations = int(get_parameter(cur, "nations"))
print_info("nations: %d" % nations)

if len(natffer) != nations:
    print_error("%d nations registred!" % len(natffer))
    raise ValueError("nations number not correct")

for i,n in enumerate(natffer):
    query = "SELECT %s FROM nodes WHERE %s>0" % (n[0], n[0])
    cur.execute(query)
    popffer = cur.fetchall()
    pop = sum([c[0] for c in popffer])
    print(i, n[0], int(pop))
