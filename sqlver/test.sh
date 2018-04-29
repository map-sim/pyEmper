#! /bin/bash

# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# application: EMPER simulator
# brief: economic and strategic simulator
# opensource licence: GPL-3.0

# ./extract_tmap.py example.db --border=FFFFFF --brightness=0.5 > tmap.ppm
# ./extract_nmap.py example.db --palette=red-blue.json ANK:FF8888 RCL:FF0000 DUQ:880000 > node.ppm

./calc_transit.py example.db ANK RCL DUQ

# geeqie node.ppm
