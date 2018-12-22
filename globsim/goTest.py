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

# handler.setParam("base_fee", 1.5)
# handler.setParam("current_fee", 1.5)
# handler.setParam("transship_fee", 2.5)

inBorder = handler.diagram.getInBorderAtoms("AGK", "NFY")
length = len(inBorder)

info = f"border length: {length}"
printInfo(info)

inBorder = handler.diagram.getInBorderAtoms("NFY", "AGK")
length = len(inBorder)




val = handler.diagram.calcTransitResistance("LTH", "QBX", "SJO")
printInfo(f"LTH QBX SJO {val}")

val = handler.diagram.calcTransitResistance("SJO", "QBX", "LTH")
printInfo(f"SJO QBX LTH {val}")


val = handler.diagram.calcTransitResistance("AZW", "RFI", "NQJ")
printInfo(f"AZW RFI NQJ {val}")

val = handler.diagram.calcTransitResistance("NQJ", "RFI", "AZW")
printInfo(f"NQJ RFI AZW {val}")

val = handler.diagram.calcTransitResistance("XXX", "YYY", "ZZZ")
printInfo(f"XXX YYY ZZZ {val}")


info = f"border length: {length}"
printInfo(info)
