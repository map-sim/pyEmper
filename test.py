#! /usr/bin/python3

from loader import EmpDiagramLoader 
from terrain import EmpTerrains 

import sys
if len(sys.argv)<3:
    raise ValueError("no input files")    

terrains = EmpTerrains(sys.argv[1])
loader = EmpDiagramLoader(terrains, sys.argv[2])
diagram = loader.get_diagram()

t = terrains.get_by_name("flat plain")
t.rgb = (0x44, 0xcc, 0x66)

t = terrains.get_by_name("great river")
t.rgb = (0x77, 0x11, 0x88)

t = terrains.get_by_name("narrow river")
t.rgb = (0xbb, 0x22, 0xff)


terrains.save("out-"+sys.argv[1])
diagram.save("out-"+sys.argv[2])
