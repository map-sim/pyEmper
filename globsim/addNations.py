#! /usr/bin/python3.7
#
# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# opensource licence: GPL-3.0
# application: GLOBSIM

from basicToolBox import printWarning
from basicToolBox import printInfo
from basicSQL import BasicSQL
import sqlite3

def addNation(database, nation):
    handler = BasicSQL(database)

    try:
        query = "CREATE TABLE nation_sm (node text unique)"
        handler.execute(query)
    except sqlite3.OperationalError:
        printWarning("nation_sm already exists?")
    
    try:
        query = "CREATE TABLE nation_st (name text unique, employment real)"
        handler.execute(query)
    except sqlite3.OperationalError:
        printWarning("nation_st already exists?")
    
    rows = handler.select("diagram_cm", "node")
    nodenames = set()
    for row in rows:
        nodenames.add(row[0])
    printInfo(f"node number: {len(nodenames)}")
    
    for node in nodenames:
        try:
            handler.insert("nation_sm", f"'{node}'")
            printInfo(node)
        except sqlite3.OperationalError: pass
        except sqlite3.IntegrityError: pass
            
    query = f"ALTER TABLE nation_sm ADD COLUMN {nation} real"
    handler.execute(query)
    
    query = f"INSERT INTO nation_st VALUES ('{nation}', 0.75)"
    handler.execute(query)
    
    query = f"UPDATE nation_sm SET {nation}=0"
    handler.execute(query)
    
import sys
database = sys.argv[1]

import random
import string    

nations = set()
nations.add("KAFR")
nations.add("VICT")
nations.add("TROJ")
nations.add("LAZR")
nations.add("SCEP")
nations.add("GERS")

while len(nations) < 16:
    nationname = ""
    for _ in range(4):
        letter = random.choice(string.ascii_uppercase)
        nationname = nationname + letter
    nations.add(nationname) 
    
for nationname in nations:
    addNation(database, nationname)
    printInfo(f"nation: {nationname}")
    
