#! /bin/bash

# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# application: EMPER simulator
# brief: economic and strategic simulator
# opensource licence: GPL-3.0

./calc_transit.py example.db ANK RCL DUQ
./extract_nmap.py example.db ANK RCL DUQ  > node.ppm
geeqie node.ppm
