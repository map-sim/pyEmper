#! /usr/bin/python3

import sys
if len(sys.argv)<2:
    raise ValueError("no input files")    

import json
dc = open(sys.argv[1])
conf = json.load(dc)

from loader import EmpDiagramLoader 
from terrain import EmpTerrains 

terrains = EmpTerrains(conf["terrains"])
loader = EmpDiagramLoader(terrains, conf["params"])
diagram = loader.get_diagram()

# t = terrains.get_by_name("cold tundra")
# t.rgb = (0x99, 0xaa, 0xbb)

from saver import EmpSaver
saver = EmpSaver()

saver["terrains"] = terrains
saver.set_param("diagram", diagram, "out-map.ppm")
saver.save("out-"+sys.argv[1])
