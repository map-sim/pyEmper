#! /usr/bin/python3

# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# opensource licence: LGPL

import os

from diagram import EmpAtom
from diagram import EmpNode

from diagram import EmpDiagram
from terrain import EmpTerrains

def readline(fd):
    line = fd.readline()
    while "#" in line:
        line = fd.readline()
    return line

def RGBreader(fd):
    index = 0
    while True:
        try:
            r = int(readline(fd))
            g = int(readline(fd))
            b = int(readline(fd))
            yield index, (r, g, b)
            index += 1
        except ValueError:
            break

class EmpDiagramLoader:
    def __init__(self, tarrains, params, nodes):        
        if not isinstance(tarrains, (EmpTerrains, )):
            raise TypeError("no terrain collection")
        self.rgb2t = dict((t.rgb, t) for t in tarrains.values())
        self.terrains = tarrains
        self.nodes = nodes
        
        fname = params["diagram ppm"]
        if not os.path.exists(fname):
            raise ValueError("file %s not exists" % fname)
        if fname[-4:] != ".ppm" and  fname[-4:] != ".PPM":
            raise ValueError("file %s not looks as PPM" % fname)
        self.fname = str(fname)
        
    def get_nearest(self, rgb):
        tmp = [(t - rgb, t) for t in self.terrains.values()]
        tmp = min(tmp, key=lambda e: e[0])
        return tmp[1]

    def create_nodes(self, world):
        active = set()
        for n in self.nodes:
            node = EmpNode()
            for x, y, p in n["skeleton"]:
                active.add(world.diagram.atoms[x][y])
                world.diagram.atoms[x][y].tmp["n"] = node
                world.diagram.atoms[x][y].tmp["p"] = float(p)
                print("*", x, y, p, world.diagram.atoms[x][y].t.name)
        print("---------")

        while True:
            try: atom = active.pop()
            except KeyError:
                break
            
            for atom2 in world.diagram.get_next(atom):                
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
                    
        # TODO: remove tmp
        # TODO: return nodes
        
    def get_diagram(self):
        with open(self.fname, "r") as fd:
            line = readline(fd) 
            if line[0:2] != "P3":
                raise ValueError("file %s not looks as P3" % self.fname)
            
            width, height = readline(fd).split()
            width, height = int(width), int(height)
            deep = readline(fd)
            
            diagram = EmpDiagram(width, height, deep)
            
            histogram = dict([(t.rgb, 0) for t in self.terrains.values()])
            for n, rgb in RGBreader(fd):
                try:
                    t = self.rgb2t[rgb]
                except KeyError:
                    t = self.get_nearest(rgb)
                    print("warning:", [hex(c) for c in rgb], "->", [hex(c) for c in t.rgb], t.name) 
                finally:
                    histogram[t.rgb] += 1
                    
                x = n % width
                y = n // width
                a = EmpAtom(x, y, t)
                diagram.atoms[x][y] = a
            diagram.tupling()
                
        total = width * height
        if n + 1 != total:
            raise ValueError("file %s looks crashed (px = %d)" % (self.fname, n + 1))

        cover = 0.0
        for t in self.terrains.values():
            frac = float(histogram[t.rgb]) / total
            print(t.name+"\t", "%.4f" % frac)
            cover += frac
        print("cover: %.4f\n---------" % cover)
        return diagram
