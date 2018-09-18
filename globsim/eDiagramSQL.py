#! /usr/bin/python3.7
#
# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# opensource licence: GPL-3.0
# application: GLOBSIM

from diagramSQL import DiagramSQL

class eDiagramSQL(DiagramSQL):

    def __init__(self, fname):
        super(eDiagramSQL, self).__init__(fname)

    def smoothBorder(self):
        tmpDiag = dict(self)
        counter = 0
        
        for x,y in self.keys():
            if self.isRiver(x, y):
                continue
            
            node = self[x,y][0]
            tmp = {node: 1}

            try:
                n = self[(x+1) % self.width ,y][0]
                tmp[n] += 1
            except KeyError: tmp[n] = 1
            try:
                n = self[(x-1+self.width) % self.width ,y][0]
                tmp[n] += 1
            except KeyError: tmp[n] = 1
            try:
                n = self[x ,y-1][0]
                try: tmp[n] += 1
                except KeyError: tmp[n] = 1
            except KeyError: pass
            try:
                n = self[x ,y+1][0]
                try: tmp[n] += 1
                except KeyError: tmp[n] = 1
            except KeyError: pass

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
                    
                n,t,dx,dy = self[x ,y]
                self[x ,y] =  newNode,t,dx,dy
                counter += 1
                
        return counter
