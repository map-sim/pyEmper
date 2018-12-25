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
handler.setParam("toll_current", 1.0)

inBorder = handler.diagram.getInBorderAtoms("AGK", "NFY")
length = len(inBorder)

info = f"AGK-NFY border length: {length}"
printInfo(info)


inBorder = handler.diagram.getInBorderAtoms("NFY", "AGK")
length = len(inBorder)

info = f"NFY-AGK border length: {length}"
printInfo(info)


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


val = handler.diagram.calcEnterResistance(["IRP", "LVL", "QBX"], "SJO")
printInfo(f"IRP LVL QBX SJO {val}")

val = handler.diagram.calcEnterResistance(["IRP", "QBX"], "SJO")
printInfo(f"IRP QBX SJO {val}")

val = handler.diagram.calcEnterResistance(["QBX"], "SJO")
printInfo(f"QBX SJO {val}")

val = handler.diagram.calcEnterResistance(["RFI"], "AZW")
printInfo(f"RFI AZW {val}")

val = handler.diagram.calcDistance("RFI", "AZW")
printInfo(f"RFI AZW {val}")

val = handler.diagram.calcDistance("CWL", "AUG")
printInfo(f"CWL AUG {val}")

