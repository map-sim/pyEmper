#! /usr/bin/python3.7
#
# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# opensource licence: GPL-3.0
# application: GLOBSIM

from diagramSQL import DiagramSQL
from globsimTools import printInfo

class eDiagramSQL(DiagramSQL):

    def __init__(self, fname):
        super(eDiagramSQL, self).__init__(fname)
        
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
