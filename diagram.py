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
    def __init__(self, width, height):
        if int(width) < 0 or int(height) < 0:
            raise  ValueError("width / height are wrong")
        self.height = int(height)
        self.width = int(width)

        self.atoms = [None] * self.width
        for x in range(self.width):
            self.atoms[x] = [None] * self.height
            
    def connect(self):
        for x in range(self.width):
            self.atoms[x] = tuple(self.atoms[x])
            
            for y in range(self.height):
                
                try:
                    self.atoms[x][y][(1, 0)] = self.atoms[x+1][y]
                except IndexError:
                    self.atoms[x][y][(1, 0)] = None

                try:
                    self.atoms[x][y][(0, 1)] = self.atoms[x][y+1]
                except IndexError:
                    self.atoms[x][y][(0, 1)] = None

                try:
                    self.atoms[x][y][(-1, 0)] = self.atoms[x-1][y]
                except IndexError:
                    self.atoms[x][y][(-1, 0)] = None
                
                try:
                    self.atoms[x][y][(0, -1)] = self.atoms[x][y-1]
                except IndexError:
                    self.atoms[x][y][(0, -1)] = None
                
        self.atoms = tuple(self.atoms)
