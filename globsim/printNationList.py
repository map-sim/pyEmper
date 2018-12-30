#! /usr/bin/python3.7
#
# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# opensource licence: GPL-3.0
# application: GLOBSIM

import sys
database = sys.argv[1]

from globsimSQL import GlobSimSQL
from basicToolBox import printInfo

handler = GlobSimSQL(database)
nations = handler.getNationList()
nodes = handler.diagram.getNodeSet()
cache = {}

for nation in nations:
    for node in nodes:
        val = handler.graph[node, nation]
        try: cache[nation] += val
        except KeyError:
            cache[nation] = val

printInfo("nations:")
for nation in cache.keys():
    printInfo(f"{nation}: {cache[nation]}")
