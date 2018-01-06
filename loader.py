#! /usr/bin/python3

import os

from diagram import EmpAtom
from diagram import EmpDiagram

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
            raise StopIteration


class EmpDiagramLoader:
    def __init__(self, tarrains, fname):        
        self.rgb2t = dict([(t.rgb, t) for t in tarrains])
        
        if not isinstance(tarrains, (set, )):
            raise TypeError("no terrain collection")
        self.terrains = tarrains
        
        if not os.path.exists(fname):
            raise ValueError("file %s not exists" % fname)
        if fname[-4:] != ".ppm" and  fname[-4:] != ".PPM":
            raise ValueError("file %s not looks as PPM" % fname)
        self.fname = str(fname)
        
    def get_nearest(self, rgb):
        tmp = [(t - rgb, t) for t in self.terrains]
        tmp = min(tmp, key=lambda e: e[0])
        return tmp[1]
        
    def get_diagram(self):
        with open(self.fname, "r") as fd:
            line = readline(fd) 
            if line[0:2] != "P3":
                raise ValueError("file %s not looks as P3" % self.fname)
            
            width, height = readline(fd).split()
            width, height = int(width), int(height)
            deep = readline(fd)
            
            diagram = EmpDiagram(width, height, deep)
            
            histogram = dict([(t.rgb, 0) for t in self.terrains])
            for n, rgb in RGBreader(fd):
                try:
                    t = self.rgb2t[rgb]
                except KeyError:
                    t = self.get_nearest(rgb)
                    print("warning:", rgb, "-->", t.rgb)
                                    
                histogram[t.rgb] += 1
                    
                x = n % width
                y = n // width
                a = EmpAtom(x, y, t)
                diagram.atoms[x][y] = a
                a.n = n
                
        total = width * height
        if n + 1 != total:
            raise ValueError("file %s not looks crashed (px = %d)" % (self.fname, n + 1))

        cover = 0.0
        for t in self.terrains:
            frac = float(histogram[t.rgb]) / total
            print(t.name+"\t", "%.4f" % frac)
            cover += frac
        print("cover: %.4f" % cover)
        diagram.connect()
        return diagram
