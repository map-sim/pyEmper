#! /usr/bin/python3

from loader import EmpMapLoader 
from terrain import EmpTerrains 

import sys
if len(sys.argv)<3:
    raise ValueError("no input files")    

terrains = EmpTerrains(sys.argv[1])
loader = EmpMapLoader(terrains, sys.argv[2])
diagram = loader.get_diagram()

t = terrains.get_by_name("costal sea")
t.rgb = (0xff, 0x0, 0xff)
print(t)

terrains.save("out-"+sys.argv[1])
