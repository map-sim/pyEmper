#! /usr/bin/python3

import sys
if len(sys.argv)<2:
    raise ValueError("no input files")    

from world import EmpWorld 

world = EmpWorld(sys.argv[1])

# t = world.terrains["open ocean"]
# t.rgb = (0x00, 0x00, 0x00)

world.save("out")


