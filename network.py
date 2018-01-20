#! /usr/bin/python3

# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# application: EMPER simulator
# brief: economic and strategic simulator
# opensource licence: GPL-3.0

from node import EmpNode 
from termcolor import colored
import random
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
                diagram.atoms[x][y].tmp["n"] = node
                diagram.atoms[x][y].tmp["p"] = float(p)

        rivers = set()        
        while True:
            try: atom = active.pop()
            except KeyError: break
                
            for atom2 in diagram.get_next(atom):
                if atom2.t.con_water >= 0.5 and atom2.t.con_ground > 0.5:
                    rivers.add(atom2)

                if atom.t.con_water < 0.5 and atom2.t.con_water < 0.5:
                    # ground process (exept rivers)
                    np = atom.tmp["p"] * atom2.t.con_ground  
                elif atom.t.con_ground == 0 and atom2.t.con_ground == 0:
                    # water process (exept rivers)                    
                    np = atom.tmp["p"] * atom2.t.con_water  
                else: continue
                
                if np > atom2.tmp["p"]:
                    atom2.tmp["p"] = np
                    atom2.tmp["n"] = atom.tmp["n"]
                    active.add(atom2)

        tmp = rivers
        rivers = set()
        tested = set()
        while True:
            try: atom = tmp.pop()
            except KeyError: break
            rivers.add(atom)
            tested.add(atom)
            
            for atom2 in diagram.get_next(atom):
                if atom2.t.con_water >= 0.5 and atom2.t.con_ground > 0.5:
                    if not atom2 in tested:
                        tmp.add(atom2)
                    
        while True:
            try: atom = rivers.pop()
            except KeyError: break
            
            nn = [a.tmp["n"] for a in diagram.get_next(atom) if a.tmp["n"] != None]
            
            if not nn: rivers.add(atom)
            else: atom.tmp["n"] = random.choice(nn)
                
                    
        # TODO: remove tmp
        # TODO: return nodes
        print(colored("(new)", "red"), "EmpNetwork")


    def save(self, fname):
        with open(fname, "w") as fd:
            conf = [n.get_config() for n in self]
            json.dump(conf, fd)
            
        print(colored("(info)", "red"), "save nodes as:", fname)
