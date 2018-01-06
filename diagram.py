#! /usr/bin/python3

class EmpAtom(dict):
    def __init__(self, x, y, t):
        if x < 0 or y < 0:
            raise ValueError("x < 0 or y < 0")
        self.x, self.y = x, y
        self.t = t
        
    def __str__(self):
        return "atom: %d %d %s" % (self.x, self.y, self.t.name)


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
            
    def save(self, fname):
        with open(fname, "w") as fd:
            fd.write("P3\n")
            fd.write("# author: Krzysztof Czarnecki\n")
            fd.write("%d %d\n" % (self.width, self.height))
            fd.write("%d\n" % self.deep)

            for y in range(self.height):
                for x in range(self.width):
                    fd.write("%d\n%d\n%d\n" % self.atoms[x][y].t.rgb)
                    
    def connect(self):
        for x in range(self.width):
            self.atoms[x] = tuple(self.atoms[x])
            
            for y in range(self.height):
                for dxy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    try:
                        self.atoms[x][y][dxy] = self.atoms[x+dxy[0]][y+dxy[1]]
                    except IndexError:
                        self.atoms[x][y][dxy] = None
                
        self.atoms = tuple(self.atoms)
