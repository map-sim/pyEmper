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
                active.add(diagram.atoms[x][y])
                diagram.atoms[x][y].n = node
                diagram.atoms[x][y].tmp["p"] = float(p)

        while True:
            try: atom = active.pop()
            except KeyError: break
                
            for atom2 in diagram.get_next(atom):
                if atom.t.con_water < 0.5 and atom2.t.con_water < 0.5:
                    # ground process (exept rivers)
                    np = atom.tmp["p"] * atom2.t.con_ground  
                elif atom.t.con_ground == 0 and atom2.t.con_ground == 0:
                    # water process (exept rivers)                    
                    np = atom.tmp["p"] * atom2.t.con_water  
                else: continue
                
                if np > atom2.tmp["p"]:
                    atom2.tmp["p"] = np
                    atom2.n = atom.n
                    active.add(atom2)

        rivers = set()        
        for row in diagram.atoms:
            for a in row:
                if a.t.con_water >= 0.5 and a.t.con_ground > 0.5:
                    rivers.add(a)
                    
        rivers = list(rivers)
        counter = 0
        while True:            
            counter += 1
            if len(rivers):
                atom = rivers.pop(counter%len(rivers))
            else: break
            
            ng = [a.n for a in diagram.get_next(atom) if a.t.con_ground>0 and a.n is not None]

            if ng: atom.n = ng[counter%len(ng)]
            else: rivers.append(atom)

        for row in diagram.atoms:
            for a in row:
                a.n.add(a)
                delattr(a, "tmp")
                if not a.n:
                    print(colored("(err)", "red"), "no node:", a.x, a.y, a.t.name)
                    raise ValueError("Nodes do not cover the entire map!")
                
        print(colored("(new)", "red"), "EmpNetwork")


    def save(self, fname):
        with open(fname, "w") as fd:
            conf = [n.get_config() for n in self]
            json.dump(conf, fd)
            
        print(colored("(info)", "red"), "save nodes as:", fname)
