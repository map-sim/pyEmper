#! /usr/bin/python3

class EmpAtom:
    def __init__(self, x, y, t):
        if x < 0 or y < 0:
            raise ValueError("x < 0 or y < 0")
        self.x, self.y = x, y
        self.t = t

        self.tmp = {}
        self.tmp["n"] = None
        self.tmp["p"] = 0.0
    
    def __str__(self):
        return "atom: %d %d %s" % (self.x, self.y, self.t.name)

class EmpNode:
    def __init__(self):
        pass
    
class EmpDiagram:
    def __init__(self, width, height, deep):
        if int(width) < 0 or int(height) < 0 or int(deep) < 0:
            raise  ValueError("width / height / deep are wrong")
        
        self.height = int(height)
        self.width = int(width)
        self.deep = int(deep)
        
        self.atoms = [None] * self.width
        for x in range(self.width):
            self.atoms[x] = [None] * self.height

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

    def rand_nodes(self, nr):
        points = []
        probability = []

        class xy:
            def __init__(self, x, y):
                self.x, self.y = x, y
                
        for y in range(self.height):
            for x in range(self.width):
                
                a = self.atoms[x][y]
                if a.t.con_ground != 0.0 and a.t.con_water >= 0.5:
                    continue
                elif a.t.con_ground == 0.0:
                    points.append(xy(x, y)) 
                    probability.append(1.5 - a.t.con_water)
                else:
                    points.append(xy(x, y))
                    probability.append(1.5 - a.t.con_ground)

        m = sum(probability)
        for n,p in enumerate(probability):
            probability[n] = float(p)/m

        import numpy
        s = set(numpy.random.choice(a=points, size=nr, p=probability))
        out = [{"skeleton": [(p.x, p.y, 1)]} for p in s]
        return out
        
    def save(self, fname, nodes, border=True):
        with open(fname, "w") as fd:
            fd.write("P3\n")
            fd.write("# author: Krzysztof Czarnecki\n")
            fd.write("%d %d\n" % (self.width, self.height))
            fd.write("%d\n" % self.deep)
            
            points = set()
            for n in nodes:
                for p in n["skeleton"]:
                    points.add((p[0], p[1])) 
            
            
            for y in range(self.height):
                for x in range(self.width):
                    try:
                        if not border:
                            raise IndexError
                        
                        if self.atoms[x][y].tmp["n"] != self.atoms[x][y+1].tmp["n"] or self.atoms[x][y].tmp["n"] != self.atoms[x][y-1].tmp["n"] \
                           or self.atoms[x][y].tmp["n"] != self.atoms[x+1][y].tmp["n"] or self.atoms[x][y].tmp["n"] != self.atoms[x-1][y].tmp["n"]:
                            fd.write("%d\n%d\n%d\n" % (0, 255, 255))
                        elif (x, y) in points:
                            fd.write("%d\n%d\n%d\n" % (255, 255, 255))
                        else:
                            raise IndexError
                    except IndexError:
                        fd.write("%d\n%d\n%d\n" % self.atoms[x][y].t.rgb)
                        
        print("(info) save diagram as:", fname)
                    
    def tupling(self):
        for x in range(self.width):
            self.atoms[x] = tuple(self.atoms[x])                
        self.atoms = tuple(self.atoms)
