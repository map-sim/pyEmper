#! /usr/bin/python3

# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# application: EMPER simulator
# brief: economic and strategic simulator
# opensource licence: GPL-3.0

from tools import *


class TerrainAutoDict(dict):
    
    def __init__(self, cur):
        self.cur = cur
        super().__init__()
        
    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        
        except KeyError:
            
            query = "SELECT color,base,ship,build,cost FROM terrains"
            self.cur.execute(query)
            raw = self.cur.fetchall()
            for color,base,ship,build,cost in raw:
                self[color] = (base,ship,build,cost)                
            print_info("terrains loaded")
            
            TerrainAutoDict.__getitem__ = dict.__getitem__
            return self[key]


class DiagramAutoDict(dict):

    def __init__(self, cur):
        self.cur = cur
        super().__init__()

    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        
        except KeyError:
            
            query = "SELECT x,y,node,color FROM atoms"
            self.cur.execute(query)
            raw = self.cur.fetchall()
            for x,y,node,color in raw:
                self[(x,y)] = (node,color)                
            print_info("diagram loaded")

            DiagramAutoDict.__getitem__ = dict.__getitem__
            return self[key]

