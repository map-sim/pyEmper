#! /usr/bin/python3.7
#
# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# opensource licence: GPL-3.0
# application: GLOBSIM

import math

from diagramSQL import DiagramSQL
from basicToolBox import printInfo
from basicToolBox import printWarning


class XiagramSQL(DiagramSQL):

    def __init__(self, fname):
        super(XiagramSQL, self).__init__(fname)
        
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
    
    def smoothCurrent(self, nodelist):
        tmpDiag = dict()
        
        for x,y in self.keys():
            if not self[x,y][0] in nodelist:
                continue
            
            landFlag = self.isLand(x, y)
            tmpx = self[x, y][2]
            tmpy = self[x, y][3]
            counter = 1

            try:
                nx, ny = (x+1) % self.width ,y
                if self.isLand(x, y) != landFlag:
                    raise KeyError             
                val = self[nx, ny]
                if val is None:
                    raise KeyError
                tmpx += val[2]
                tmpy += val[3]                
                counter += 1
            except KeyError: pass

            try:
                nx, ny = (x-1+self.width) % self.width ,y
                if self.isLand(x, y) != landFlag:
                    raise KeyError 
                val = self[nx, ny]
                if val is None:
                    raise KeyError
                tmpx += val[2]
                tmpy += val[3]                
                counter += 1
            except KeyError: pass

            try:
                nx, ny = x, y-1
                if self.isLand(x, y) != landFlag:
                    raise KeyError 
                val = self[nx, ny]
                if val is None:
                    raise KeyError
                tmpx += val[2]
                tmpy += val[3]                
                counter += 1
            except KeyError: pass
        
            try:
                nx, ny = x, y+1
                if self.isLand(x, y) != landFlag:
                    raise KeyError
                val = self[nx, ny]
                if val is None:
                    raise KeyError
                tmpx += val[2]
                tmpy += val[3]                
                counter += 1
            except KeyError: pass

            dx, dy = tmpx/counter, tmpy/counter
            tmpDiag[x,y] = self[x, y][0], self[x, y][1], dx, dy

        self.debug = False
        self.direct = False
        for x,y in self.keys():
            if not self[x,y][0] in nodelist:
                continue            
            if tmpDiag[x,y][2] != self[x, y][2] or tmpDiag[x,y][3] != self[x, y][3]: 
                self[x,y] = tmpDiag[x,y]
        self.direct = True
        self.debug = True
        printInfo("smooth current")
            
    def smoothBorder(self):
        counter = 0
        
        for x,y in self.keys():
            if self.isRiver(x, y):
                continue
            
            node = self[x,y][0]
            tmp = {node: 1}

            try:
                n = self[x+1 ,y][0]
                tmp[n] += 1
            except KeyError: tmp[n] = 1
            try:
                n = self[x-1 ,y][0]
                tmp[n] += 1
            except KeyError: tmp[n] = 1
            
            val = self[x, y-1]
            if val:
                try: tmp[val[0]] += 1
                except KeyError:
                    tmp[val[0]] = 1

            val = self[x, y+1]
            if val:
                try: tmp[val[0]] += 1
                except KeyError:
                    tmp[val[0]] = 1

            newNode = None
            for n in tmp.keys():
                if tmp[n] >= 3:
                    newNode = n                
            if newNode is None:
                continue
                    
            if newNode != node:
                zo = self.isLand(node)
                zn = self.isLand(newNode)
                if zo != zn: continue
                    
                n,t,dx,dy = self[x, y]
                self[x ,y] =  newNode,t,dx,dy
                counter += 1
                
        return counter

