#! /usr/bin/python3.7
#
# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# opensource licence: GPL-3.0
# application: GLOBSIM

import math
from configSQL import ConfigSQL
from basicToolBox import str2rgb

from basicToolBox import printError
from basicToolBox import printWarning

class DiagramSQL(ConfigSQL, dict):

    def __init__(self, fname):
        ConfigSQL.__init__(self, fname)
        dict.__init__(self)
        
        self.width = self.getParam("map_width")
        self.height = self.getParam("map_height")
        
        rows = self.select("diagram_cm")        
        for x,y,n,t,dx,dy in rows:
            dict.__setitem__(self, (x,y), (n,t,dx,dy))

        self.maxdrag = 0.0
        self.terrains = dict()
        rows = self.select("terrain_ct")        
        for name, color, drag, charge, aperture in rows:
            self.terrains[color] = name, drag, charge, aperture
            if abs(drag) > self.maxdrag:
                self.maxdrag = abs(drag)
                
    def __getitem__(self, key):
        x, y = key
        x += self.width
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

    def getNodeSet(self): # TO UPDATE
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
        aperture = self.terrains[color][3]
        if bool(aperture) and drag < 0:
            return True
        return False
        
    def isLand(self, nx, y=None):
        if y is None:
            x, y = self.getFirstAtom(nx)
        else: x = nx
        
        color = self[x,y][1]
        aperture = self.terrains[color][3]
        return bool(aperture)

    def isSee(self, nx, y=None):
        if y is None:
            x, y = self.getFirstAtom(nx)
        else: x = nx
        
        color = self[x,y][1]
        aperture = self.terrains[color][3]
        return not bool(aperture)

    def calcArea(self, node):
        test = f"node='{node}'"
        rows = self.select("diagram_cm", "x,y", test=test)
        return len(rows) * self.getParam("map_scale") 
    
    def calcAperture(self, node):
        test = f"node='{node}'"
        points = self.select("diagram_cm", "color", test=test)
        aperture = 0.0
        for color in points:
            test = f"color='{color[0]}'"
            rows = self.select("terrain_ct", "aperture", test=test)
            aperture += rows[0][0]            
        return aperture * self.getParam("map_scale") 
    
    def calcCharge(self, node):
        test = f"node='{node}'"
        points = self.select("diagram_cm", "color", test=test)
        drag, counter = 0.0, 0
        for color in points:
            test = f"color='{color[0]}'"
            rows = self.select("terrain_ct", "charge", test=test)
            drag += rows[0][0]
            counter += 1
        return drag / counter  

    def calcCapacity(self, node):
        test = f"node='{node}'"
        points = self.select("diagram_cm", "color", test=test)
        capacity = 0.0
        for color in points:
            test = f"color='{color[0]}'"
            rows = self.select("terrain_ct", "aperture,charge", test=test)
            capacity += rows[0]["aperture"] / rows[0]["charge"]
        return capacity  * self.getParam("map_scale")
            
    def calcMean(self, node):
        test = f"node='{node}'"
        rows = self.select("diagram_cm", "x,y", test=test)
        xm, ym, count = 0.0, 0.0, 0
        for x,y in rows:
            count += 1
            xm += x
            ym += y
        xm /= count
        ym /= count
        return xm, ym
    
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
                if yo < 0 or yo >= self.height: continue
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
    
    def __calcResistance(self, xo, yo, xe, ye):
        nO,tO,dxO,dyO = self[xo, yo]           
        nE,tE,dxE,dyE = self[xe, ye]
        rO = self.terrains[tO][1]
        rE = self.terrains[tE][1]

        rOUT = abs(rE) * self.getParam("toll_transport")

        cX = math.copysign(1, (xe - xo) * dxE)
        cY = math.copysign(1, (ye - yo) * dyE)
        currf = self.getParam("toll_current")
        cX *= currf
        cY *= currf

        rOUT **= (1.0 + cX)
        rOUT **= (1.0 + cY)
        
        if rO * rE < 0:
            # rOUT += abs(rE/rO) **  math.copysign(1, rE) * self.getParam("toll_transship")
            rOUT += abs(rE-rO) * self.getParam("toll_transship")
            
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
                nx, ny = (x + jx+ self.width) % self.width, y + jy
                if ny < 0 or ny >= self.height: continue
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
        discontinuity = 0
        for x,y in rows:
            try:
                out += plazma[x, y]
                counter += 1
            except KeyError:
                discontinuity += 1
        if discontinuity:
            printWarning(f"{stop} discontinuity: {discontinuity}")
            
        out = math.sqrt(out)
        out *= self.getParam("map_scale")
        return out
    
    def calcDistance(self, start, stop):
        xo, yo = self.calcMean(start)
        xe, ye = self.calcMean(stop)
        
        d2 = (xo - xe) ** 2 + (yo - ye) ** 2
        d = math.sqrt(d2) * self.getParam("map_scale")
        return d
    
    def getVicinity(self, node):
        output = set()
        test = f"node='{node}'"
        rows = self.select("diagram_cm", "x,y", test=test)        
        for x,y in rows:
            if not self.checkNext(x, y, node):
                continue
            for dx, dy in [(0,1), (0,-1), (1,0), (-1,0)]:
                try:
                    tnode = self.getNode(x+dx, y+dy)
                except TypeError: continue
                
                if tnode != node:
                    output.add(tnode)
        return output
