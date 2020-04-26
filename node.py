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
parser.add_option("-p", "--province", dest="province",
                  help="point nodes")
parser.add_option("-x", "--xnode", dest="xnode",
                  action="store_true", default=False,
                  help="print xnode mode")
parser.add_option("-m", "--margin", dest="margin",
                  help="margin/padding", default=0)
parser.add_option("-s", "--stream", dest="stream",
                  help="stream resistance")
parser.add_option("-l", "--list", dest="listv",
                  action="store_true", default=False,
                  help="print mode list")
parser.add_option("-t", "--type", dest="type", default="all",
                  help="terrain type: sea, land, all")
opts, args = parser.parse_args()

###
### main
###

import BusyBoxSQL, math
driver = BusyBoxSQL.BusyBoxSQL(opts.dbfile)

if opts.province is not None and not opts.xnode:
    ToolBox.print_output(f"node: {opts.province}")
    atoms = driver.get_node_atoms_as_dict(opts.province)
    ToolBox.print_output(f"atoms: {len(atoms)}")
    scale = driver.get_config_by_name("map_scale")
    ToolBox.print_output(f"area: {len(atoms)*scale}")

    terrains = {}
    aperture = 0.0
    for atom in atoms.values():
        if atom[0] not in terrains.keys():
            terr = driver.get_terrain_as_dict(atom[0])
            terrains[atom[0]] = terr
        aperture += terrains[atom[0]]["aperture"]
    ToolBox.print_output(f"aperture: {aperture*scale}")
    
    popdict = driver.get_population_by_node_as_dict(opts.province)
    pop = sum([v for k,v in popdict.items() if k != "node"])
    ToolBox.print_output(f"population: {pop}")
    for k,v in popdict.items():
        if k == "node": continue
        if v == 0: continue
        ToolBox.print_output(f"   + {k}: {v}")

    prod = driver.calc_production(opts.province)    
    ToolBox.print_output(f"production: {prod}")
        
    # p = driver.get_config_by_name("production_factor")
    # r, f = driver.get_distribution_as_list(opts.province, "resourcing", "industry")
    # production = p * math.sqrt(pop) * r * ((f + 1.0) / (f + aperture))
    # ToolBox.print_output(f"production: {production}")

    
elif opts.province is not None and opts.xnode:
    xyset = driver.get_node_coordinates_as_set(opts.province)
    m = int(opts.margin)

    w = min(xyset, key=lambda x: x[0])
    e = max(xyset, key=lambda x: x[0])
    s = max(xyset, key=lambda x: x[1])
    n = min(xyset, key=lambda x: x[1])
    print(f"-s{s[1]+m} -n{n[1]-m} -w{w[0]-m} -e{e[0]+m}")

elif opts.listv:
    if opts.type == "all":
        nodes = driver.get_node_names_as_set()
    elif opts.type == "see":
        diagram = driver.get_vector_diagram()
        nodes = [n for n in driver.get_node_names_as_set() if not diagram.check_land(n)]
    elif opts.type == "land":
        diagram = driver.get_vector_diagram()
        nodes = [n for n in driver.get_node_names_as_set() if diagram.check_land(n)]
    elif opts.type == "capital":
        dout = driver.get_controls_as_dict("capital")
        if opts.xnode:
            nodes = "-".join([cap[0] for cap in dout.values()])
        else:
            nodes = [f"{cap[0]} -> {ctrl}" for ctrl, cap in dout.items()]        
    else: raise ValueError(f"Unkown type: {opts.type}. Available: see, land, capital, or all.")
    if not opts.xnode:
        for node in nodes:
            ToolBox.print_output(node)
    else: print(nodes)
            
elif opts.stream:
    nodes = opts.stream.split("-")
    assert len(nodes) > 1, "(e) at least 2 provinces (X-Y-Z...) are needed"
    diagram = driver.get_vector_diagram()

    rin = diagram.calc_enter_resistance(nodes[1], nodes[0])
    ToolBox.print_output(f"in: {nodes[0]} --> {nodes[1]} = {rin}")
    total = rin

    for p, t, n in zip(nodes, nodes[1:], nodes[2:]):
        rt = diagram.calc_transit_resistance(p, t, n)
        ToolBox.print_output(f"{p} --> {t} --> {n} = {rt}")
        total += rt
        
    rout = diagram.calc_enter_resistance(nodes[-2], nodes[-1])
    ToolBox.print_output(f"out: {nodes[-2]} --> {nodes[-1]} = {rout}")
    total += rout

    ToolBox.print_output(f"end-end: {nodes[0]} --> {nodes[-1]} = {total}")

else:  # summary
    nodes = driver.get_node_names_as_set()
    diagram = driver.get_vector_diagram()
    totalatoms = len(diagram)

    buildset = set()
    buildatoms = 0
    coastatoms = 0
    naviatoms = 0

    for xy in diagram.keys():
        if diagram.check_buildable(*xy):
            buildset.add(diagram.get_node(*xy))
            buildatoms += 1
        if diagram.check_navigable(*xy) or diagram.check_coast(*xy):
            naviatoms += 1
        if diagram.check_coast(*xy):
            coastatoms += 1

    na = 100 * float(naviatoms)/totalatoms
    fa = 100 * float(buildatoms)/totalatoms
    ca = 100 * float(coastatoms)/totalatoms
    ToolBox.print_output(f"total nodes: {len(nodes)}")
    ToolBox.print_output(f"buildable nodes: {len(buildset)} area: {fa} %")
    ToolBox.print_output(f"coast length: {coastatoms} / {ca} %")
    ToolBox.print_output(f"navigable area: {na} %")

    total = 0
    people = {nat: 0 for nat in driver.get_nation_names_as_set()}
    for nat in people.keys():
        natdis = driver.get_population_as_dict(nat)
        tot = sum(natdis.values())
        people[nat] = tot
        total += tot
    ToolBox.print_output(f"total population: {total}")
    for n, p in people.items():
        frac = round(100 * float(p) / total, 3)
        ToolBox.print_output(f"   {n}: {p} {frac} %")
        
