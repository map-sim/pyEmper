#! /usr/bin/python3

# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# application: EMPER simulator
# brief: economic and strategic simulator
# opensource licence: GPL-3.0

from node import EmpNode 
from termcolor import colored
import json
import math

class EmpNetwork(list):
    def __init__(self, diagram, fname):
        self.world = diagram.world
        self.diagram = diagram
        with open(fname) as dc:
            conf = json.load(dc)

        active = set()
        for raw in conf:
            node = EmpNode(raw)
            self.append(node)
            for x, y, p in raw["skeleton"]:
                active.add(self.diagram[x][y])
                self.diagram[x][y].n = node
                self.diagram[x][y].tmp["p"] = float(p)

        while True:
            try: atom = active.pop()
            except KeyError: break
                
            for atom2 in self.diagram.get_next(atom):
                if atom.t.isground() and atom2.t.isground():
                    np = atom.tmp["p"] * atom2.t.con_base
                    if atom2.t.isriver() or atom.t.isriver():
                        np *= self.world.conf["transship con"]
                elif atom.t.iswater() and atom2.t.iswater():
                    np = atom.tmp["p"] * atom2.t.con_delta  
                else: continue
                
                np *= self.world.conf["transport con"]
                if np > atom2.tmp["p"]:
                    atom2.tmp["p"] = np
                    atom2.n = atom.n
                    active.add(atom2)

        g = self.diagram.get_agener()
        for a in g():
            if a.n is None:
                print(colored("(err)", "red"), "no node:", a.x, a.y, a.t.name)
                raise ValueError("Nodes do not cover the entire map!")
            del(a.tmp["p"])
            a.n.add(a)
                
        print(colored("(new)", "red"), "EmpNetwork")

    def get_enter_cost(self, start_nodes, stop_node, transport_infra=0, fortress_infra=0):
        tmp = set()
        active = set()
        for atom in stop_node:
            for node in start_nodes:
                if node in [an.n for an in self.diagram.get_next(atom)]:
                    atom.tmp["t"] = 1.0
                    active.add(atom)
                    tmp.add(atom)
                
        while active:
            try: atom = active.pop()
            except KeyError: break
            
            for atom2 in self.diagram.get_next(atom):
                if not (atom.n is stop_node) and not (atom2.n is stop_node):
                    continue                    
                elif atom.t.isground() and atom2.t.isground():
                    np = atom.tmp["t"] * (atom2.t.con_base + atom2.t.con_delta * transport_infra) * (1.0 - fortress_infra)
                    if atom2.t.isriver() and not atom.t.isriver() or not atom2.t.isriver() and atom.t.isriver():
                        np *= self.world.conf["transship con"]
                elif atom.t.iswater() and atom2.t.isground():
                    np = atom.tmp["t"] * (atom2.t.con_base + atom2.t.con_delta * transport_infra) * (1.0 - fortress_infra)
                    np *= self.world.conf["transship con"]
                elif atom.t.isground() and atom2.t.iswater():
                    np = atom.tmp["t"] * atom2.t.con_delta
                    np *= self.world.conf["transship con"]
                else:
                    np = atom.tmp["t"] * atom2.t.con_delta

                np *= self.world.conf["transport con"]
                if np > atom2.tmp["t"]:
                    atom2.tmp["t"] = np
                    active.add(atom2)
                    tmp.add(atom2)

        output = 0.0
        for atom in tmp:
            if atom.n is stop_node:
                output += -math.log10(atom.tmp["t"])
            atom.tmp["t"] = 0.0
        return output

            
    def save(self, fname):
        with open(fname, "w") as fd:
            conf = [n.get_config() for n in self]
            json.dump(conf, fd)
            
        print(colored("(info)", "red"), "save nodes as:", fname)
