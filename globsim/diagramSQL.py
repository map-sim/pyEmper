#! /usr/bin/python3.7
#
# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# opensource licence: GPL-3.0
# application: GLOBSIM

import math
from configSQL import ConfigSQL
from basicToolBox import printError
from basicToolBox import str2rgb

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
        self.maxdrag = 0.0
        rows = self.select("terrain_ct")        
        for name, color, drag, charge in rows:
            self.terrains[color] = name, drag, charge
            if abs(drag) > self.maxdrag:
                self.maxdrag = abs(drag)
                
    def __getitem__(self, key):
        x, y = key
        x %= self.width
        if y < 0 or y >= self.height: return None
        else: return dict.__getitem__(self, (x, y))
        
    def __setitem__(self, key, value):
        x, y = key
        x %= self.width
        if y < 0 or y >= self.height:
            return        
        
        test = f"x={x} AND y={y}"
        nval = f"node='{value[0]}', color='{value[1]}'"         
        if len(value) == 4:         
            dict.__setitem__(self, (x, y), value)
            dnum = f"dx={value[2]}, dy={value[3]}"
            self.update("diagram_cm", f"{dnum}, {nval}", test)

        elif len(value) == 2:
            val = *value, self[x,y][2], self[x,y][3]
            dict.__setitem__(self, (x, y), val)
            self.update("diagram_cm", f"{nval}", test)
            
        else:
            printError("diagram has to have 4/2-length items!")
            raise TypeError("item len")

    def getNodeSet(self):
        outSet = set()        
        for x,y in self.keys():
            outSet.add(self[x,y][0])
        return outSet
    
    def checkNext(self, x, y, node):
        if node == self[x+1,y][0]: return True
        if node == self[x-1,y][0]: return True
        try:
            if node == self[x,y+1][0]: return True
        except TypeError: pass
        try:
            if node == self[x,y-1][0]: return True
        except TypeError: pass
        return False
    
    def getNode(self, x, y):
        return self[x,y][0]
    
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
            x, y = self.getFirstAtom(nx)
        else: x = nx
        
        color = self[x,y][1]
        charge = self.terrains[color][2]
        return bool(charge)

    def isSee(self, nx, y=None):
        if y is None:
            x, y = self.getFirstAtom(nx)
        else: x = nx
        
        color = self[x,y][1]
        charge = self.terrains[color][2]
        return not bool(charge)

    def getFirstAtom(self, node):
        test = f"node='{node}'"
        rows = self.select("diagram_cm", "x,y", test=test)        
        return rows[0][0], rows[0][1]

    def getInBorderAtoms(self, start, stop):        
        test = f"node='{start}'"
        rows = self.select("diagram_cm", "x,y", test=test)
        inBorder = set()
        for x,y in rows:
            x1, x2 = x + 1, x - 1
            y1, y2 = y + 1, y - 1
            for xo, yo in [(x, y1), (x, y2), (x1, y), (x2, y)]:
                try:
                    if self[xo, yo][0] == stop:
                        inBorder.add((x, y))
                        continue
                except KeyError: pass                
        return inBorder
    
    def checkBeach(self, x, y):        
        return self.isRiver(x, y) or self.checkCoast(x, y)
        
    def checkBorder(self, x, y):
        x1, x2 = x + 1, x - 1
        y1 = (y + 1) % self.height
        y2 = (y - 1) % self.height
        OUT, LMask, UMask, DMask, RMask = 0, 8, 4, 2, 1        
        if self[x, y][0] != self[x1, y][0]: OUT |= RMask 
        elif self[x, y][0] != self[x2, y][0]: OUT |= LMask
        elif self[x, y][0] != self[x, y1][0]: OUT |= UMask 
        elif self[x, y][0] != self[x, y2][0]: OUT |= DMask 
        return OUT

    def checkCoast(self, x, y):
        x1, x2 = x + 1, x - 1 
        y1 = (y + 1) % self.height
        y2 = (y - 1) % self.height
        OUT, LMask, UMask, DMask, RMask = 0, 8, 4, 2, 1        
        if self.isLand(x, y) != self.isLand(x1, y): OUT |= RMask 
        elif self.isLand(x, y) != self.isLand(x2, y): OUT |= LMask
        elif self.isLand(x, y) != self.isLand(x, y1): OUT |= UMask 
        elif self.isLand(x, y) != self.isLand(x, y2): OUT |= DMask 
        return OUT
    
    def getTerrColor(self, x, y):
        return str2rgb(self[x,y][1])
    
    def getCurrColor(self, x, y):
        if self[x,y][2] == 0 and self[x,y][3] == 0:
            color = self[x,y][1]
            drag = self.terrains[color][1]
            
            if drag < 0.0:
                r = 191 + 40 * (self.maxdrag+drag) / self.maxdrag
                g = 191 + 40 * (self.maxdrag+drag) / self.maxdrag
                b = 191 + 40 * (self.maxdrag+drag) / self.maxdrag
            else:
                r = 215 - 40 * drag / self.maxdrag
                g = 215 - 40 * drag / self.maxdrag
                b = 215 - 40 * drag / self.maxdrag

        else:
            angle = math.atan2(self[x,y][2], self[x,y][3])
            angle /= math.pi
            r, g, b = 0, 0, 0
            if angle > 0 and angle <= 0.5:
                r = 255
                b = 255 * angle * 2
            elif angle > 0.5:
                r = 255 * (0.5 - (angle - 0.5)) * 2 
                b = 255
            elif angle > -0.5:
                a = - 2 * angle
                r = 255 - 128 * a
                g = 200 * a
            else:
                a = - 2 * (angle + 0.5)
                g = 200 * (1 - a)
                r = 170 * (1 - a)
                b = 255 * a            
                
            module = math.sqrt(self[x,y][2]**2 + self[x,y][3]**2)
            r = r + (255.9 - r) * (1.0 - module)
            g = g + (255.9 - g) * (1.0 - module)
            b = b + (255.9 - b) * (1.0 - module)
            
        return int(r), int(g), int(b)
