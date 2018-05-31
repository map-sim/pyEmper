#! /bin/bash

# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# application: EMPER simulator
# brief: economic and strategic simulator
# opensource licence: GPL-3.0

./verify_database.py example.db

# ./dump_tables.sh example.db
# ./find_partial.py example.db

./list_params.py example.db
./list_nations.py example.db
./list_building.py example.db
./list_terrains.py example.db
./list_resources.py example.db

./extract_tmap.py example.db tmap.ppm --resize=2 --border=0.5 --median

./extract_pmap.py example.db pmap-xio.ppm --palette=default.json --resize=2 --rivers --median XIO
./extract_pmap.py example.db pmap-vag.ppm --palette=default.json --resize=2 --rivers --median VAG
./extract_pmap.py example.db pmap-cet.ppm --palette=default.json --resize=2 --rivers --median CET
./extract_pmap.py example.db pmap-rao.ppm --palette=default.json --resize=2 --rivers --median RAO
./extract_pmap.py example.db pmap-squ.ppm --palette=default.json --resize=2 --rivers --median SQU
./extract_pmap.py example.db pmap-zup.ppm --palette=default.json --resize=2 --rivers --median ZUP
./extract_pmap.py example.db pmap-var.ppm --palette=default.json --resize=2 --rivers --median VAR
./extract_pmap.py example.db pmap-jop.ppm --palette=default.json --resize=2 --rivers --median JOP
./extract_pmap.py example.db pmap-tty.ppm --palette=default.json --resize=2 --rivers --median TTY
./extract_pmap.py example.db pmap-erg.ppm --palette=default.json --resize=2 --rivers --median ERG
./extract_pmap.py example.db pmap-ace.ppm --palette=default.json --resize=2 --rivers --median ACE
./extract_pmap.py example.db pmap-quz.ppm --palette=default.json --resize=2 --rivers --median QUZ
./extract_pmap.py example.db pmap-tyr.ppm --palette=default.json --resize=2 --rivers --median TYR
./extract_pmap.py example.db pmap-gea.ppm --palette=default.json --resize=2 --rivers --median GEA
./extract_pmap.py example.db pmap-pau.ppm --palette=default.json --resize=2 --rivers --median PAU
./extract_pmap.py example.db pmap-loo.ppm --palette=default.json --resize=2 --rivers --median LOO
./extract_pmap.py example.db pmap-par.ppm --palette=default.json --resize=2 --rivers --median PAR
./extract_pmap.py example.db pmap-foy.ppm --palette=default.json --resize=2 --rivers --median FOY

# ./gener_smap.py example.db RENEW 771188:10 BB22FF:8 FFAA11:5 FFDD44:3 FF4400:2 884400:1 COAST:3 BUILDABLE:1
# ./gener_smap.py example.db STONE 440022:50 884400:50 FF4400:10 FFAA11:1 FFDD44:0.3 TUNDR:0.2 COAST:0.2 BUILDABLE:1
# ./gener_smap.py example.db AGRA 771188:25 BB22FF:25 448844:5 33BB33:20 FFAA11:10 884400:-0.1 FFDD44:0.07 COAST:20 HLINE:210 SIGMA:9600 THOLD:0.06 BUILDABLE:1
# ./gener_smap.py example.db WOOD 771188:30 BB22FF:30 448844:30 33BB33:18 FFAA11:2 COAST:20 AAAA99:-20 FFDD44:-0.2 HLINE:230 SIGMA:9200 THOLD:0.2 BUILDABLE:1
# ./gener_smap.py example.db FISH 0000CC:20 0044FF:18 0077FF:10 771188:12 BB22FF:6 448844:8 33BB33:1 HLINE:235 SIGMA:29200 THOLD:0.1 COAST:1

./extract_smap.py example.db smap-stone.ppm --resize=2 --palette=default.json --median --rivers STONE
./extract_smap.py example.db smap-renew.ppm --resize=2 --palette=default.json --median --rivers RENEW
./extract_smap.py example.db smap-gold.ppm --resize=2 --palette=default.json --median --rivers GOLD
./extract_smap.py example.db smap-wood.ppm --resize=2 --palette=default.json --median --rivers WOOD
./extract_smap.py example.db smap-agra.ppm --resize=2 --palette=default.json --median --rivers AGRA
./extract_smap.py example.db smap-coal.ppm --resize=2 --palette=default.json --median --rivers COAL
./extract_smap.py example.db smap-rare.ppm --resize=2 --palette=default.json --median --rivers RARE
./extract_smap.py example.db smap-fish.ppm --resize=2 --palette=default.json --median --rivers FISH
./extract_smap.py example.db smap-ore.ppm --resize=2 --palette=default.json --median --rivers ORE
./extract_smap.py example.db smap-oil.ppm --resize=2 --palette=default.json --median --rivers OIL

./extract_nmap.py example.db nmap-1.ppm --resize=1 --palette=default.json --rivers --median MZG:880000 HMB DUQ BGY GOU GOP OXS MRH BJO ZBD GXR GDV:880000
./calc_chain.py example.db MZG HMB DUQ BGY GOU GOP OXS MRH BJO ZBD GXR GDV

./extract_nmap.py example.db nmap-2.ppm --resize=1 --palette=default.json --rivers --median MZG:880000 ANK QNT GTP JJA ZYQ YQF NYU BFN XJK ODT GDV:880000
./calc_chain.py example.db MZG ANK QNT GTP JJA ZYQ YQF NYU BFN XJK ODT GDV

./extract_nmap.py example.db nmap-3.ppm --resize=1 --palette=default.json --rivers --median MZG:880000 BYG QDF IQA NCO TCA NQB VYW XBS GXR GDV:880000
./calc_chain.py example.db MZG BYG QDF IQA NCO TCA NQB VYW XBS GXR GDV


