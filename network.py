#! /usr/bin/python3

# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# application: EMPER simulator
# brief: economic and strategic simulator
# opensource licence: GPL-3.0

from node import EmpNode 
from termcolor import colored
import json

class EmpNetwork(list):
    def __init__(self, diagram, fname):
        with open(fname) as dc:
            conf = json.load(dc)

        active = set()
        for raw in conf:
            node = EmpNode(raw)
            self.append(node)
            for x, y, p in raw["skeleton"]:
                active.add(diagram[x][y])
                diagram[x][y].n = node
                diagram[x][y].tmp["p"] = float(p)

        while True:
            try: atom = active.pop()
            except KeyError: break
                
            for atom2 in diagram.get_next(atom):
                if atom.t.isground() and atom2.t.isground():
                    np = atom.tmp["p"] * atom2.t.con_ground
                    if atom2.t.isriver() or atom.t.isriver():
                        np *= 0.1
                elif atom.t.iswater() and atom2.t.iswater():
                    np = atom.tmp["p"] * atom2.t.con_water  
                else: continue
                
                if np > atom2.tmp["p"]:
                    atom2.tmp["p"] = np
                    atom2.n = atom.n
                    active.add(atom2)

        g = diagram.get_agener()
        for a in g():
            if a.n is None:
                print(colored("(err)", "red"), "no node:", a.x, a.y, a.t.name)
                raise ValueError("Nodes do not cover the entire map!")
            delattr(a, "tmp")
            a.n.add(a)
                
        print(colored("(new)", "red"), "EmpNetwork")

    def get_transport_cost(self, start_node, stop_node):
        return 0
    
    def save(self, fname):
        with open(fname, "w") as fd:
            conf = [n.get_config() for n in self]
            json.dump(conf, fd)
            
        print(colored("(info)", "red"), "save nodes as:", fname)
