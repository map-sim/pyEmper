#! /bin/bash

# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# application: EMPER simulator
# brief: economic and strategic simulator
# opensource licence: GPL-3.0

./extract_tmap.py example.db tmap.ppm --resize=2 --border=0.5
./extract_nation_nmap.py example.db loo.ppm --palette=default.json --resize=2 --rivers LOO
./extract_nation_nmap.py example.db par.ppm --palette=default.json --resize=2 --rivers PAR


./extract_nmap.py example.db node-2.ppm --resize=2 --palette=default.json --rivers  MZG:880000 HMB DUQ BGY GOU GOP OXS MRH BJO ZBD GDV:880000
./calc_chain.py example.db MZG HMB DUQ BGY GOU GOP OXS MRH BJO ZBD GDV

./extract_nmap.py example.db node-3.ppm --resize=2 --palette=default.json --rivers MZG:880000 ANK QNT GTP JJA ZYQ YQF NYU BFN XJK ODT GDV:880000
./calc_chain.py example.db MZG ANK QNT GTP JJA ZYQ YQF NYU BFN XJK ODT GDV







# geeqie node.ppm
