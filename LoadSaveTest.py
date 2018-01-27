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

t = world.terrains["ice ocean"]
t.rgb = (0x0, 0x77, 0xff)

t = world.terrains["cold tundra"]
t.rgb = (0xaa, 0xaa, 0x99)

t = world.terrains["flat plain"]
t.rgb = (0x33, 0xbb, 0x33)

t = world.terrains["dry desert"]
t.rgb = (0xff, 0xdd, 0x44)

t = world.terrains["high plateau"]
t.rgb = (0xff, 0xaa, 0x11)

world.save("output.save")


