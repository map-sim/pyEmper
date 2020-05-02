#! /usr/bin/python3.7
#
# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# opensource licence: GPL-3.0
# application: GLOBSIM

###
### opt parsing
###

import optparse, os
import ToolBox

parser = optparse. OptionParser()
parser.add_option("-f", "--db-file", dest="dbfile",
                  metavar="FILE", default="demo.sql",
                  help="saved simulator state")
opts, args = parser.parse_args()

###
### main
###

import BusyBoxSQL
driver = BusyBoxSQL.BusyBoxSQL(opts.dbfile)
diagram = driver.get_vector_diagram()

land_nodes = [n for n in driver.get_node_names_as_set() if diagram.check_land(n)]
sea_nodes = [n for n in driver.get_node_names_as_set() if not diagram.check_land(n)]        

for node in land_nodes:
    control = driver.calc_control(node)
    prod = driver.calc_production(node)    
    print(node, prod, [(c, round(v, 3)) for c, v in control.items() ])

    
