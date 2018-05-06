#! /bin/bash

# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# application: EMPER simulator
# brief: economic and strategic simulator
# opensource licence: GPL-3.0

./extract_tmap.py example.db tmap.ppm --resize=2 --border=0.5

./extract_nmap.py example.db node-1.ppm --resize=2 --palette=default.json --rivers ANK:880000 RCL DUQ BGY GOU GOP OXS MRH KAD KJZ GDV:880000
./calc_transit.py example.db ANK RCL DUQ BGY GOU GOP OXS MRH KAD KJZ GDV

./extract_nmap.py example.db node-2.ppm --resize=2 --palette=default.json  --rivers 1 2 3 4 7 8 11 14
./extract_nation_nmap.py example.db par.ppm --palette=default.json --resize=2 --rivers PAR

# geeqie node.ppm
