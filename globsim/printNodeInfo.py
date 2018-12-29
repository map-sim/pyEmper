#! /usr/bin/python3.7
#
# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# opensource licence: GPL-3.0
# application: GLOBSIM

import sys
database = sys.argv[1]
nodename = sys.argv[2]

from globsimSQL import GlobSimSQL
from basicToolBox import printInfo

handler = GlobSimSQL(database)
printInfo(f"name: {nodename}")

area = handler.diagram.calcArea(nodename)
cap = handler.diagram.calcCapacity(nodename)
mean = handler.diagram.calcMean(nodename)

printInfo(f"area: {area}")
printInfo(f"capacity: {cap}")
printInfo(f"mean: {mean}")




