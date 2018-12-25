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
printInfo(f"area: {area}")


