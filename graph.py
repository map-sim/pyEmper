#! /usr/bin/python3

# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# application: EMPER simulator
# brief: economic and strategic simulator
# opensource licence: GPL-3.0

from toolbox import measure_time
from termcolor import colored

from node import EmpNode 
import json, math

class EmpGraph(list):
    @measure_time("graph init")
    def __init__(self, diagram, fname):
        self.world = diagram.world
        self.diagram = diagram
        with open(fname) as dc:
            conf = json.load(dc)

        plazma = {}
        active = set()
        for name in conf.keys():
            node = EmpNode(name, conf[name])
            self.append(node)
            
            for x, y, p in conf[name]["skeleton"]:
                plazma[self.diagram[x][y]] = float(p)
                active.add(self.diagram[x][y])
                self.diagram[x][y].n = node

        while True:
            try: atom = active.pop()
            except KeyError: break
                
            for a2 in self.diagram.get_next(atom):
                if atom.t.isground() and a2.t.isground():
                    np = plazma[atom] * a2.t.con_base
                    if a2.t.isriver() or atom.t.isriver():
                        np *= self.world.conf["transship"]
                elif atom.t.iswater() and a2.t.iswater():
                    np = plazma[atom] * a2.t.con_delta
                else: continue
                
                np *= self.world.conf["transport"]
                if not a2 in plazma.keys() or np > plazma[a2]:
                    plazma[a2] = np
                    a2.n = atom.n
                    active.add(a2)

        g = self.diagram.get_agener()
        for a in g():
            if a.n is None:
                print(colored("(err)", "red"), "no node:", a.x, a.y, a.t.name)
                raise ValueError("Nodes do not cover the entire map!")
            a.n.add(a)
        print(colored("(new)", "red"), "EmpGraph")
        
    def get_proxy_cost(self, start, proxy, stop, transport_infra=0):
        plazma = {}
        active = set()
        for atom in proxy:
            if start in [an.n for an in self.diagram.get_next(atom)]:
                plazma[atom] = (1.0, None)
                active.add(atom)
                
        while active:
            try: atom = active.pop()
            except KeyError: break

            for a2 in self.diagram.get_next(atom):
                if not (atom.n is proxy) and not (a2.n is proxy):
                    continue                    

                elif atom.t.isground() and a2.t.isground():
                    np = plazma[atom][0] * (a2.t.con_base + a2.t.con_delta * transport_infra)                    
                    if a2.t.isriver() and not atom.t.isriver() or not a2.t.isriver() and atom.t.isriver():
                        np *= self.world.conf["transship"]
                elif atom.t.iswater() and a2.t.isground():
                    np = plazma[atom][0] * (a2.t.con_base + a2.t.con_delta * transport_infra)
                    np *= self.world.conf["transship"]
                elif atom.t.isground() and a2.t.iswater():
                    np = plazma[atom][0] * a2.t.con_delta
                    np *= self.world.conf["transship"]
                else:
                    np = plazma[atom][0] * a2.t.con_delta
                    
                np *= self.world.conf["transport"]
                if not a2 in plazma.keys():
                    plazma[a2] = (0.0, None) 
                    
                if np > plazma[a2][0]:
                    plazma[a2] = (np, atom)                    
                    active.add(a2)

        target = set()
        for atom in proxy:
            if stop in [an.n for an in self.diagram.get_next(atom)]:
                target.add(atom)

        output = 0.0
        for atom in target:
            a2 = atom 
            if not a2 in  plazma.keys():
                break

            while plazma[a2][1]:
                output += -math.log10(plazma[a2][0])
                a2 = plazma[a2][1]
                
        try: return output / len(target)
        except ZeroDivisionError:
            return 0.0
        
    def get_enter_cost(self, start_nodes, stop_node, transport_infra=0, fortress_infra=0):
        plazma = {}
        active = set()
        for atom in stop_node:            
            for node in start_nodes:
                if node in [a2.n for a2 in self.diagram.get_next(atom)]:
                    plazma[atom] = (1.0, None)
                    active.add(atom)

        while active:
            try: atom = active.pop()
            except KeyError: break
            
            for a2 in self.diagram.get_next(atom):
                if not (atom.n is stop_node) and not (a2.n is stop_node):
                    continue                    
                elif atom.t.isground() and a2.t.isground():
                    np = plazma[atom][0] * (a2.t.con_base + a2.t.con_delta * transport_infra) * (1.0 - fortress_infra)
                    if a2.t.isriver() and not atom.t.isriver() or not a2.t.isriver() and atom.t.isriver():
                        np *= self.world.conf["transship"]
                elif atom.t.iswater() and a2.t.isground():
                    np = plazma[atom][0] * (a2.t.con_base + a2.t.con_delta * transport_infra) * (1.0 - fortress_infra)
                    np *= self.world.conf["transship"]
                elif atom.t.isground() and a2.t.iswater():
                    np = plazma[atom][0] * a2.t.con_delta
                    np *= self.world.conf["transship"]
                else:
                    np = plazma[atom][0] * a2.t.con_delta

                np *= self.world.conf["transport"]
                if not a2 in plazma.keys():
                    plazma[a2] = (0.0, None) 

                if np > plazma[a2][0]:
                    plazma[a2] = (np, atom)                    
                    active.add(a2)

        output = 0.0
        for atom in plazma.keys():
            if atom.n is stop_node:
                output += -math.log10(plazma[atom][0])
        return output
        
    def save(self, fname):
        with open(fname, "w") as fd:
            conf = {}
            for n in self:
                conf[n.name] = n.get_config()
            json.dump(conf, fd)
            
        print(colored("(info)", "red"), "save nodes as:", fname)

    def get_max_population(self):
        return max([n.get_population() for n in self])
    
    def get_max_density(self):
        return max([n.get_density() for n in self])
                
