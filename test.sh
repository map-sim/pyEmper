#! /bin/bash

# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# application: EMPER simulator
# brief: economic and strategic simulator
# opensource licence: GPL-3.0

./verify_database.py example.db
./dump_tables.sh example.db

./list_params.py example.db
./list_nations.py example.db
./list_terrains.py example.db

./extract_tmap.py example.db tmap.ppm --resize=1 --border=0.5 
./extract_pmap.py example.db pmap-loo.ppm --palette=default.json --resize=2 --rivers LOO
./extract_pmap.py example.db pmap-par.ppm --palette=default.json --resize=2 --rivers PAR


./extract_nmap.py example.db nmap-2.ppm --resize=1 --palette=default.json --rivers  MZG:880000 HMB DUQ BGY GOU GOP OXS MRH BJO ZBD GDV:880000
./calc_chain.py example.db MZG HMB DUQ BGY GOU GOP OXS MRH BJO ZBD GDV

./extract_nmap.py example.db nmap-3.ppm --resize=1 --palette=default.json --rivers MZG:880000 ANK QNT GTP JJA ZYQ YQF NYU BFN XJK ODT GDV:880000
./calc_chain.py example.db MZG ANK QNT GTP JJA ZYQ YQF NYU BFN XJK ODT GDV







# geeqie node.ppm
