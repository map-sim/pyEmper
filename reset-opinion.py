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
controls = driver.get_controls_as_dict("nation")
nations = driver.get_nation_names_as_set()

updated = 0
for control, nation in controls.items():
    for n in nations:
        val = 1.0 if nation[0] == n else 0.0
        driver.set_opinion_by_control(control, n, val)
    updated += 1
ToolBox.print_output(f"updated: {updated}")

###
### init capital nodes for each control
###

driver.set_capital_node("HAN-0", "QYO")
driver.set_capital_node("HAN-1", "VJD")
driver.set_capital_node("HAN-2", "YZP")

driver.set_capital_node("TUR-0", "RCL")
driver.set_capital_node("TUR-1", "KAK")
driver.set_capital_node("TUR-2", "XYZ")
driver.set_capital_node("TUR-3", "BGY")

driver.set_capital_node("LAT-0", "GDV")
driver.set_capital_node("LAT-1", "WVI")
driver.set_capital_node("LAT-2", "DKC")

driver.set_capital_node("INK-0", "USM")
driver.set_capital_node("INK-1", "GIE")
driver.set_capital_node("INK-2", "KVH")

driver.set_capital_node("PER-0", "UUG")
driver.set_capital_node("PER-1", "KAD")

driver.set_capital_node("ISM-0", "OET")
driver.set_capital_node("ISM-1", "GDM")
driver.set_capital_node("ISM-2", "NYU")

driver.set_capital_node("JAP-0", "UEM")
driver.set_capital_node("JAP-1", "HTS")
driver.set_capital_node("JAP-2", "HTS")
driver.set_capital_node("JAP-3", "BJM")

driver.set_capital_node("BUD-0", "QEV")
driver.set_capital_node("BUD-1", "QZD")

driver.set_capital_node("CEL-0", "BHH")
driver.set_capital_node("CEL-1", "TQT")

driver.set_capital_node("SUN-0", "DTY")
driver.set_capital_node("SUN-1", "KRP")

driver.set_capital_node("IND-0", "OCP")
driver.set_capital_node("IND-1", "AXL")
driver.set_capital_node("IND-2", "YPH")

driver.set_capital_node("SLO-0", "BYG")
driver.set_capital_node("SLO-1", "BYG")
driver.set_capital_node("SLO-2", "OSL")

driver.set_capital_node("GER-0", "UEF")
driver.set_capital_node("GER-1", "CCD")

driver.set_capital_node("ZUL-0", "IFG")
driver.set_capital_node("ZUL-1", "ULH")
driver.set_capital_node("ZUL-2", "FFI")

driver.set_capital_node("SAS-0", "FZV")
driver.set_capital_node("SAS-1", "IWI")

driver.set_capital_node("NOR-0", "RYQ")
driver.set_capital_node("NOR-1", "FCD")
