#! /usr/bin/python3

# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# application: EMPER simulator
# brief: economic and strategic simulator
# opensource licence: GPL-3.0


import sys, os
import sqlite3

from tools import get_parameter
from termcolor import colored

if not os.path.exists(sys.argv[1]):
    error = colored("(error)", "red")
    print(error, "path %s not exists!" % sys.argv[1])
    raise ValueError("database not exists")

conn = sqlite3.connect(sys.argv[1])
print(colored("database:", "green"), sys.argv[1])
cur = conn.cursor()

query = "SELECT * FROM nations"
cur.execute(query)
natffer = cur.fetchall()

nations = int(get_parameter(cur, "nations"))
print(colored("nations:", "green"), nations)

if len(natffer) != nations:
    error = colored("(error)", "red")
    print(error, "%d nations registred!" % len(natffer))
    raise ValueError("nations number not correct")


for i,n in enumerate(natffer):
    query = "SELECT %s FROM nodes WHERE %s>0" % (n[0], n[0])
    cur.execute(query)
    popffer = cur.fetchall()
    pop = sum([c[0] for c in popffer])
    print(i, n[0], int(pop))
