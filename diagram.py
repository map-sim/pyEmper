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


class EmpDiagram:
    def __init__(self, terrains, fname):

        if not isinstance(terrains, (EmpTerrains, )):
            raise TypeError("no terrain collection")
        self.rgb2t = dict((t.rgb, t) for t in terrains.values())
        hist = dict([(t.rgb, 0) for t in terrains.values()])

        width, height, generator = PPMloader(fname)
        if int(width) < 0 or int(height) < 0:
            raise  ValueError("width / height are wrong")
        
        self.width = int(width)
        self.height = int(height)        
        self.atoms = [None] * self.width
        for x in range(self.width):
            self.atoms[x] = [None] * self.height
        
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
            self.atoms[x][y] = a
        self.tupling()
                
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

    def tupling(self):
        for x in range(self.width):
            self.atoms[x] = tuple(self.atoms[x])                
        self.atoms = tuple(self.atoms)

    def get_next(self, a):
        out = []
        try: out.append(self.atoms[a.x][a.y+1])
        except IndexError: pass
        try: out.append(self.atoms[a.x][a.y-1])
        except IndexError: pass
        try: out.append(self.atoms[a.x+1][a.y])
        except IndexError: pass
        try: out.append(self.atoms[a.x-1][a.y])
        except IndexError: pass
        return out
        
    def save(self, fname, border=True):
        with open(fname, "w") as fd:
            fd.write("P3\n")
            fd.write("# author: Krzysztof Czarnecki\n")
            fd.write("%d %d\n" % (self.width, self.height))
            fd.write("255\n")
            
            for y in range(self.height):
                for x in range(self.width):
                    try:
                        if not border:
                            raise IndexError
                        
                        if self.atoms[x][y].tmp["n"] != self.atoms[x][y+1].tmp["n"] or self.atoms[x][y].tmp["n"] != self.atoms[x][y-1].tmp["n"] \
                           or self.atoms[x][y].tmp["n"] != self.atoms[x+1][y].tmp["n"] or self.atoms[x][y].tmp["n"] != self.atoms[x-1][y].tmp["n"]:
                            nrgb = [ c + (255-c)*0.75 if sum(self.atoms[x][y].t.rgb) < 16 else 0.333 * c for c in self.atoms[x][y].t.rgb]                            
                            fd.write("%d\n%d\n%d\n" % tuple(nrgb))
                        else:
                            raise IndexError
                        
                    except IndexError:
                        fd.write("%d\n%d\n%d\n" % self.atoms[x][y].t.rgb)
                        
        print(colored("(info)", "red"), "save diagram as:", fname)
                    
