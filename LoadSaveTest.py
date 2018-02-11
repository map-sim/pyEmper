#! /usr/bin/python3

# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# application: EMPER simulator
# brief: economic and strategic simulator
# opensource licence: GPL-3.0

import sys
if len(sys.argv)<2:
    raise ValueError("no input files")    

from world import EmpWorld 
world = EmpWorld(sys.argv[1])

# t = world.terrains["ice ocean"]
# t.rgb = (0x0, 0x77, 0xff)

world.save("output.save")


