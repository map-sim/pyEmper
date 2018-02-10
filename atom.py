#! /usr/bin/python3

# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# application: EMPER simulator
# brief: economic and strategic simulator
# opensource licence: GPL-3.0


class EmpAtom:
    def __init__(self, x, y, t):
        if x < 0 or y < 0:
            raise ValueError("x < 0 or y < 0")
        self.x, self.y = x, y
        self.t = t
        self.n = None
    
    def __str__(self):
        return "atom: %d %d %s" % (self.x, self.y, self.t.name)
