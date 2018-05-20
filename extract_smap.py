#! /usr/bin/python3

# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# application: EMPER simulator
# brief: economic and strategic simulator
# opensource licence: GPL-3.0

import sys, os
from tools import print_info

cmd = ["python3 extract_map.py"]
for arg in sys.argv[1:]: 
    cmd.append(arg)

cmd[-1] = "smap"
cmd.append(sys.argv[-1])
strcmd = "".join([c+" " for c in cmd])

print_info(strcmd)
os.system(strcmd)
