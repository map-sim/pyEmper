#! /bin/bash

# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# application: EMPER simulator
# brief: economic and strategic simulator
# opensource licence: GPL-3.0

# ./extract_tmap.py example.db --border=FFFFFF --brightness=0.5 > tmap.ppm

# ./extract_nmap.py example.db --resize=2 --palette=red-blue.json ANK:FF8888 RCL:FF0000 DUQ:880000 > node.ppm
./calc_transit.py example.db ANK RCL DUQ
./calc_transit.py example.db DUQ RCL ANK

# ./extract_nmap.py example.db --resize=1 --palette=red-blue.json  AVI MAG FPQ > node.ppm
./calc_transit.py example.db AVI MAG FPQ
./calc_transit.py example.db FPQ MAG AVI

# geeqie node.ppm
