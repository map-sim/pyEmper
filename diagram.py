#! /usr/bin/python3

# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# application: EMPER simulator
# brief: economic and strategic simulator
# opensource licence: GPL-3.0

from terrain import EmpTerrains 
from ppm import PPMloader 
from atom import EmpAtom 

from termcolor import colored


class EmpDiagram(list):
    def __init__(self, terrains, fname):
        list.__init__(self)
        self.world = terrains.world
        if not isinstance(terrains, (EmpTerrains, )):
            raise TypeError("no terrain collection")
        self.rgb2t = dict((t.rgb, t) for t in terrains.values())
        hist = dict([(t.rgb, 0) for t in terrains.values()])

        width, height, generator = PPMloader(fname)
        if int(width) < 0 or int(height) < 0:
            raise  ValueError("width / height are wrong")
        
        self.width = int(width)
        self.height = int(height)        
        for x in range(self.width):
            self.append([None] * self.height)
        
        for n, rgb in generator:
            try:
                t = self.rgb2t[rgb]
            except KeyError:
                t = terrains.get_nearest(rgb)
                print("warning:", [hex(c) for c in rgb], "->", [hex(c) for c in t.rgb], t.name) 
            finally:
                hist[t.rgb] += 1
                    
            x = n % width
            y = n // width
            a = EmpAtom(x, y, t)
            self[x][y] = a
                
        total = width * height
        if n + 1 != total:
            raise ValueError("file %s looks crashed (px = %d)" % (self.fname, n + 1))

        cover = 0.0
        for t in terrains.values():
            frac = float(hist[t.rgb]) / total
            print(t.name+"\t", "%.4f" % frac)
            cover += frac
        print("cover: %.4f" % cover)
        print(colored("(new)", "red"), "EmpDiagram")

    def get_agener(self):
        def gener():
            for y in range(self.height):
                for x in range(self.width):
                    # ny = (y + self.width) % self.height
                    # nx = (x+y) % self.width
                    # yield self[nx][ny]
                    yield self[x][y]
        return gener
    
    def get_next(self, a):
        out = []
        try: out.append(self[a.x][a.y+1])
        except IndexError: pass
        try:
            if a.y-1 < 0: raise IndexError
            out.append(self[a.x][a.y-1])
        except IndexError: pass
        try: out.append(self[a.x+1][a.y])
        except IndexError: pass
        try:
            if a.x-1 < 0: raise IndexError
            out.append(self[a.x-1][a.y])
        except IndexError: pass
        return out
        
    def isborder(self, a):
        na = self.get_next(a)
        for a2 in na:
            if not a2.n is a.n:
                return True
        return False
        
    def save(self, fname):
        with open(fname, "w") as fd:
            fd.write("P3\n")
            fd.write("# author: Krzysztof Czarnecki\n")
            fd.write("%d %d\n" % (self.width, self.height))
            fd.write("255\n")
            
            for y in range(self.height):
                for x in range(self.width):
                    fd.write("%d\n%d\n%d\n" % self[x][y].t.rgb)
                        
        print(colored("(info)", "red"), "save diagram as:", fname)
                    
