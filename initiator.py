#! /usr/bin/python3.7
#
# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# opensource licence: GPL-3.0
# application: GLOBSIM

###
### opt parsing
###

import optparse
import ToolBox

parser = optparse. OptionParser()
parser.add_option("-f", "--db-file", dest="dbfile",
                  metavar="FILE", default="demo.sql",
                  help="saved simulator state")

parser.add_option("-p", "--pocc", dest="pocc",
                  help="occurence probability")
parser.add_option("-u", "--uniform", dest="uniform",
                  help="uniform distribution Vmin:Vmax")
parser.add_option("-c", "--clean", dest="clean",
                  action="store_true", default=False,
                  help="clean all values")

parser.add_option("-d", "--delete", dest="delete",
                  help="delete nodes X-Y-Z")

parser.add_option("-n", "--next", dest="numnext",
                  help="number of next nodes N:factor")
parser.add_option("-w", "--window", dest="window",
                  help="sin window Ystart:Ystop")
parser.add_option("-b", "--btype", dest="btype", default="all",
                  help="terrain type: sea, land, all")
parser.add_option("-t", "--terrain", dest="tfunc",
                  help="terrain description RGB1:X-RGB2:Y")
parser.add_option("-e", "--extend", dest="extend",
                  help="add nodes X-Y-Z")

# parser.add_option("-D", "--distribution", dest="distribution",
#                   help="distribution values")

parser.add_option("-N", "--nation", dest="nation",
                  help="nation values")
parser.add_option("-l", "--lnorm", dest="lnorm",
                  action="store_true", default=False,
                  help="population linear norm")

parser.add_option("-m", "--migration", dest="migration",
                  help="number of migration", default=0)

opts, args = parser.parse_args()

###
### generator definition
###

import BusyBoxSQL
import random
import math

class Initiator:
    def __init__(self, dbfile, btype, what):
        self.driver = BusyBoxSQL.BusyBoxSQL(dbfile)
        self.diagram = self.driver.get_vector_diagram()
        nodes = []

        self.btype = btype
        self.nodes = nodes
        self.urange = None
        self.nfactor = 0
        self.nlength = 0
        self.wstart = 0
        self.wstop = 0
        self.tfunc = {}
        self.gocache = {}
        
    # def clean_source(self, source):
    #    self.driver.clean_source(source)

    def clean_population(self, nation):
        self.driver.clean_population(nation)

    def reduce_nodes_by_pocc(self, pocc):
        if not pocc: return
        toget = int(float(opts.pocc) * len(self.nodes))
        self.nodes = random.sample(self.nodes, toget)

    def set_uniform_range(self, ustr):
        if not ustr: return
        umin, umax = ustr.split(":")
        umin, umax = float(umin), float(umax)
        assert umin < umax, "(e) min, max"
        self.urange = umin, umax
        
    def set_next_nodes(self, nstr):
        if not nstr: return
        nlen, nfactor = nstr.split(":")
        self.nfactor = float(nfactor)
        self.nlength = int(nlen)

    def set_window(self, wstr):
        if not wstr: return
        wstart, wstop = wstr.split(":")
        assert int(wstart) < int(wstop), "(e) window"
        self.wstart = int(wstart)
        self.wstop = int(wstop)
        
    def set_terrain_function(self, tstr):
        if not tstr: return
        tlist = tstr.split("-")
        for tv in tlist:
            t, v = tv.split(":")
            self.tfunc[t] = float(v)

    def obtain_new_value(self, node):
        if self.tfunc:
            nan = True
            value = 0.0 
            xyset = self.diagram.get_node_coordinates_as_set(node)
            for xy in xyset:
                t, n, d = self.diagram[xy]
                if self.diagram.check_coast(*xy):
                    try:
                        value += self.tfunc["COAST"]
                        nan = False
                    except KeyError: pass
                try:
                    value += self.tfunc[t]
                    nan = False                    
                except KeyError: continue
            if nan:
                try: value = self.tfunc["NAN"]
                except KeyError: pass
        else: value = 1.0
        
        if self.urange:
            v = random.random()
            v *= self.urange[1] - self.urange[0]
            value *= v + self.urange[0]

        if self.wstart != self.wstop:
            x, y = self.diagram.get_node_center(node)
            if y > self.wstop: return 0 
            if y < self.wstart: return 0 
            width = self.wstop - self.wstart
            yt = float(y - self.wstart) / width
            value *= math.sin(math.pi * yt)
        return value

    def set_source(self, source):
        updated = set()
        for node in self.nodes:
            v = self.obtain_new_value(node)
            if v == 0: continue

            ov = self.driver.get_source_by_node(node, source)
            ToolBox.print_output("source:", node, source, v+ov)
            self.driver.set_source_by_node(node, source, v+ov)
            updated.add(node)
            
            nnodes = self.diagram.get_next_nodes_as_set(node)
            if self.btype == "land":
                nnodes = {n for n in nnodes if self.diagram.check_land(n)}
            elif self.btype == "sea":
                nnodes = {n for n in nnodes if not self.diagram.check_land(n)}
            nlength = self.nlength if self.nlength <= len(nnodes) else len(nnodes)
            nnodes = random.sample(nnodes, nlength)

            for nn in nnodes:
                ov = self.driver.get_source_by_node(nn, source)
                ToolBox.print_output("source:", nn, source, self.nfactor*v+ov)
                self.driver.set_source_by_node(nn, source,self.nfactor*v+ov)
                updated.add(nn)

        return len(updated)

    def set_population(self, nation):
        updated = set()
        initval = 10000
        for node in self.nodes:
            self.driver.set_population_by_node(node, nation, initval)
            updated.add(node)
        return len(updated)

    def migration(self, nation, iterations):
        allnodes = self.driver.get_node_names_as_set()
        finalcache = {}
        for _ in range(iterations):
            cache = {}
            for node in allnodes:
                try: value = finalcache[node]
                except KeyError:
                    value = self.driver.get_population_by_node(node, nation)
                    finalcache[node] = value
                    cache[node] = value 
                if value == 0: continue

                nnodes = self.diagram.get_next_nodes_as_set(node)
                for nn in nnodes: 
                    try: cost = self.gocache[node, nn]
                    except KeyError:
                        cost = self.diagram.calc_enter_resistance(node, nn)
                        self.gocache[node, nn] = math.sqrt(cost)                        
                        ToolBox.print_output(f"migration-{nation} register new cost:", node, nn, cost)

                    try: cache[nn] += float(value) / cost
                    except KeyError:
                        cache[nn] = float(value) / cost

            for node, val in cache.items():
                try: finalcache[node] += val
                except KeyError:
                    finalcache[node] = val

        for node, value in finalcache.items():
            self.driver.set_population_by_node(node, nation, int(value))
        return len(finalcache)

    def population_lnorm(self):
        popnode = self.driver.get_population_as_dict()
        nations = self.driver.get_nation_names_as_set()
        natnode = {nat: self.driver.get_population_as_dict(nat) for nat in nations}
        for node, pop in popnode.items():
            capacity = self.obtain_new_value(node)
            land = self.diagram.check_land(node)
            for nation in nations:
                if natnode[nation][node] == 0: continue
                if land:
                    value = int(capacity * natnode[nation][node] / pop)
                    self.driver.set_population_by_node(node, nation, value)
                else: self.driver.set_population_by_node(node, nation, 0)

###
### main
###

if opts.nation: what = "population"
elif opts.lnorm: what = "population"
else: raise ValueError("(e) what?")

## if opts.distribution: what = "distribution"

init = Initiator(opts.dbfile, opts.btype, what)
if opts.clean:
    if opts.nation: init.clean_population(opts.nation)
    # if opts.distribution: init.clean_distribution(opts.distribution)

init.reduce_nodes_by_pocc(opts.pocc)
if opts.extend:
    nodes = opts.extend.split("-")
    init.nodes.extend(nodes)
    
init.set_terrain_function(opts.tfunc)
init.set_uniform_range(opts.uniform)
init.set_next_nodes(opts.numnext)
init.set_window(opts.window)
        
# if opts.distribution:
#     ToolBox.print_output("updated nodes (D):", init.set_distrobution(opts.distribution))
    
if opts.nation:
    init.set_population(opts.nation)
    no = init.migration(opts.nation, int(opts.migration))
    ToolBox.print_output("updated nodes (N):", no)
    if opts.delete:
        dnodes = opts.delete.split("-")
        for node in dnodes:
            init.driver.set_population_by_node(node, opts.nation, 0)

if opts.lnorm:
    init.population_lnorm()
