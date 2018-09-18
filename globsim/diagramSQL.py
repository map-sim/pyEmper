#! /usr/bin/python3.7
#
# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# opensource licence: GPL-3.0
# application: GLOBSIM

from configSQL import ConfigSQL
from globsimTools import printError
from globsimTools import str2rgb

class DiagramSQL(ConfigSQL, dict):

    def __init__(self, fname):
        ConfigSQL.__init__(self, fname)
        dict.__init__(self)
        
        self.width = self.getParam("map_width")
        self.height = self.getParam("map_height")
        
        rows = self.select("diagram_cm")        
        for x,y,n,t,dx,dy in rows:
            dict.__setitem__(self, (x,y), (n,t,dx,dy))

        self.terrains = dict()
        rows = self.select("terrain_ct")        
        for name, color, drag, charge in rows:
            self.terrains[color] = name, drag, charge

    def __setitem__(self, key, value):
        if len(value) != 4:
            printError("diagram has to have 4-length items!")
            raise TypeError("item len")
        
        dict.__setitem__(self, key, value)
        test = f"x={key[0]} AND y={key[1]}"
        dnum = f"dx={value[2]}, dy={value[3]}"
        nval = f"{dnum}, node='{value[0]}', color='{value[1]}'"         
        self.update("diagram_cm", f"{nval}", test)
            
    def getNode(self, x, y):
        return self[x,y][0]

    def getColor(self, x, y):
        return str2rgb(self[x,y][1])
    
    def getStream(self, x, y):
        return self[x,y][2], self[x,y][3]
    
    def isRiver(self, x, y):
        color = self[x,y][1]
        drag = self.terrains[color][1]
        charge = self.terrains[color][2]
        if bool(charge) and drag < 0:
            return True
        return False
        
    def isLand(self, nx, y=None):
        if y is None:
            x, y = self.getFirstXY(nx)
        else: x = nx
        
        color = self[x,y][1]
        charge = self.terrains[color][2]
        return bool(charge)

    def isSee(self, nx, y=None):
        if y is None:
            x, y = self.getFirstXY(nx)
        else: x = nx
        
        color = self[x,y][1]
        charge = self.terrains[color][2]
        return not bool(charge)

    def getFirstXY(self, node):
        test = f"node='{node}'"
        rows = self.select("diagram_cm", "x,y", test=test)        
        return rows[0][0], rows[0][1]

    def checkBorder(self, x, y):
        x1 = (x + 1) % self.width
        y1 = (y + 1) % self.height
        x2 = (x - 1 + self.width) % self.width
        y2 = (y - 1 + self.height) % self.height
        OUT, LMask, UMask, DMask, RMask = 0, 8, 4, 2, 1        
        if self[x, y][0] != self[x1, y][0]: OUT |= RMask 
        elif self[x, y][0] != self[x2, y][0]: OUT |= LMask
        elif self[x, y][0] != self[x, y1][0]: OUT |= UMask 
        elif self[x, y][0] != self[x, y2][0]: OUT |= DMask 
        return OUT
