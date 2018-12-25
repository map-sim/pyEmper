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


class xDiagramSQL(DiagramSQL):

    def __init__(self, fname):
        super(xDiagramSQL, self).__init__(fname)
        
    def smoothCurrent(self):
        tmpDiag = dict()
        
        for x,y in self.keys():
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

    def __calcResistance(self, xo, yo, xe, ye):
        nO,tO,dxO,dyO = self[xo, yo]           
        nE,tE,dxE,dyE = self[xe, ye]
        rO = self.terrains[tO][1]
        rE = self.terrains[tE][1]

        rOUT = abs(rE) * self.getParam("toll_transport")

        cX = (xe - xo) * dxE 
        cY = (ye - yo) * dyE 
        if cX > 0: cX *= self.getParam("toll_current")        
        if cY > 0: cY *= self.getParam("toll_current")
        rOUT *= (1.0 + cX) * (1.0 + cY)
        
        if rO * rE < 0:
            rOUT += abs(rO - rE) * self.getParam("toll_transship")
            
        return rOUT

    def __plazming(self, startPoints, nodeName):
        active = set()
        plazma = dict()        
        for x,y in startPoints:            
            n,t,dx,dy = self[x, y]            
            r = self.terrains[t][1]
            plazma[x, y] = abs(r)
            active.add((x, y))
            
        while active:
            try: x, y = active.pop()
            except KeyError: break
            
            for jx,jy in [(0,1), (0,-1), (1,0), (-1,0)]:
                nx, ny = x + jx, y + jy
                if not self.checkNext(nx, ny, nodeName):
                    continue
                
                uR = self.__calcResistance(x, y, nx, ny)
                nR = plazma[x, y] + uR
                if not (nx, ny) in plazma.keys():
                    plazma[nx, ny] = nR
                    active.add((nx, ny))     
                elif nR < plazma[nx, ny]:
                    plazma[nx, ny] = nR
                    active.add((nx, ny))
                    
        return plazma
    
    def calcTransitResistance(self, start, tranz, stop):
        inBorder = self.getInBorderAtoms(start, tranz)
        outBorder = self.getInBorderAtoms(stop, tranz)
        if not len(inBorder):
            printWarning(f"no common points: {start}-{tranz}")            
            return 0
        if not len(outBorder):
            printWarning(f"no common points: {tranz}-{stop}")            
            return 0

        plazma = self.__plazming(inBorder, tranz)
        
        out = 0.0
        for x,y in outBorder:
            out += plazma[x, y]

        out *= self.getParam("map_scale")
        out /= len(outBorder)
        return out 

    def calcEnterResistance(self, starts, stop):
        inBorder = set()
        for start in starts:
            dBorder = self.getInBorderAtoms(start, stop)
            if len(dBorder) == 0:
                printWarning(f"no common points: {start}-{stop}")

            inBorder.update(dBorder)
            
        plazma = self.__plazming(inBorder, stop)

        out = 0.0
        counter = 0
        test = f"node='{stop}'"
        rows = self.select("diagram_cm", "x,y", test=test)
        for x,y in rows:
            out += plazma[x, y]
            counter += 1

        out = math.sqrt(out)
        out *= self.getParam("map_scale")
        return out
    
    def calcDistance(self, start, stop):
        xo, yo = self.calcMean(start)
        xe, ye = self.calcMean(stop)
        
        d2 = (xo - xe) ** 2 + (yo - ye) ** 2
        d = math.sqrt(d2) * self.getParam("map_scale")
        return d
