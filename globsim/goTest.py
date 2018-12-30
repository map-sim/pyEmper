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
from basicToolBox import printError

handler = GlobSimSQL(database)
# handler.setParam("toll_current", 1.0)



def calcTotalResistance(path):
    if len(path) < 2:
        printError("path len < 2")
        
    total = 0.0
    val = handler.diagram.calcEnterResistance([path[1]], path[0])
    print([path[1]], path[0], val)
    total += val
    for i, item in enumerate(path[1:-1]):
        i += 1
        p = path[i-1]
        c = item
        n = path[i+1]
        val = handler.diagram.calcTransitResistance(p, c, n)
        print(p, c, n, val)
        total += val

    val = handler.diagram.calcEnterResistance([path[-2]], path[-1])
    print([path[-2]], path[-1], val)
    total += val

    return total

path = ["SUI", "MZG", "HMB", "XYZ", "DUK", "ULC"]
res = calcTotalResistance(path)
printInfo(f"{res}: {path}")

path = list(reversed(path))
res = calcTotalResistance(path)
printInfo(f"{res}: {path}")

# 
# 
# val = handler.diagram.calcTransitResistance("LTH", "QBX", "SJO")
# printInfo(f"LTH QBX SJO {val}")
# 
# val = handler.diagram.calcTransitResistance("SJO", "QBX", "LTH")
# printInfo(f"SJO QBX LTH {val}")
# 
# 
# val = handler.diagram.calcTransitResistance("AZW", "RFI", "NQJ")
# printInfo(f"AZW RFI NQJ {val}")
# 
# val = handler.diagram.calcTransitResistance("NQJ", "RFI", "AZW")
# printInfo(f"NQJ RFI AZW {val}")
# 
# val = handler.diagram.calcTransitResistance("XXX", "YYY", "ZZZ")
# printInfo(f"XXX YYY ZZZ {val}")
# 
# val = handler.diagram.calcEnterResistance(["IRP", "LVL", "QBX"], "SJO")
# printInfo(f"IRP LVL QBX SJO {val}")
# 
# val = handler.diagram.calcEnterResistance(["IRP", "QBX"], "SJO")
# printInfo(f"IRP QBX SJO {val}")
# 
# val = handler.diagram.calcEnterResistance(["QBX"], "SJO")
# printInfo(f"QBX SJO {val}")
# 
# val = handler.diagram.calcEnterResistance(["RFI"], "AZW")
# printInfo(f"RFI AZW {val}")
# 
# 
# val = handler.diagram.calcEnterResistance(["CWL"], "HOD")
# printInfo(f"QBX SJO {val}")
# 
# 
# val = handler.diagram.calcDistance("RFI", "AZW")
# printInfo(f"RFI AZW {val}")
# 
# val = handler.diagram.calcDistance("CWL", "AUG")
# printInfo(f"CWL AUG {val}")


