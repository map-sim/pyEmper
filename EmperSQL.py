#! /usr/bin/python3

# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# application: EMPER simulator
# brief: economic and strategic simulator
# opensource licence: GPL-3.0

import sys, os
import sqlite3
import math

from tools import xy_gener
from tools import str_to_rgb

from tools import print_out
from tools import print_info
from tools import print_error

from NodeDictFactory import NodeDictFactory
from MoveEstimator import MoveEstimator
from BasicSQL import BasicSQL

from AutoDicts import TerrainAutoDict
from AutoDicts import DiagramAutoDict

    
class EmperSQL(BasicSQL, NodeDictFactory, MoveEstimator):

    def __init__(self, fname):
        super(EmperSQL, self).__init__(fname)
        
        width = int(self.get_parameter("width"))
        height = int(self.get_parameter("height"))
        print_info("size: %d x %d" % (width, height))
        
        self.terrdict = TerrainAutoDict(self.cur)
        self.diagram = DiagramAutoDict(self.cur)
                    
    def get_node_name(self, number):
        query = "SELECT name FROM population LIMIT 1 OFFSET %d" % int(number)
        self.cur.execute(query)
        return self.cur.fetchone()[0]
    
    def get_nation_name(self, number):
        query = "SELECT name FROM nations LIMIT 1 OFFSET %d" % int(number)
        self.cur.execute(query)
        return self.cur.fetchone()[0]

    def select_building(self, node, column):
        query = "SELECT %s FROM building WHERE name='%s'" % (column, node)
        self.cur.execute(query)
        return self.cur.fetchone()[0]
    
    def get_parameter(self, name):
        query = "SELECT value FROM parameters WHERE name='%s'" % name 
        self.cur.execute(query)
        return self.cur.fetchone()[0]
    
    def calc_points(self, nodename):
        g = self.nodepoints_generator(nodename)
        return len(tuple(g))
    
    def nodepoints_generator(self, nodename):
        query = "SELECT x,y FROM atoms WHERE node='%s'" % nodename
        points = self.select_many(query)
        for x,y in points:
            yield x,y
            
    def tmappoints_generator(self, border, resize):
        width = int(self.get_parameter("width"))
        height = int(self.get_parameter("height"))
        if border < 0:
            for x, y in xy_gener (width, height, resize):
                color = str_to_rgb(self.diagram[(x,y)][1])
                if self.is_border(x, y):
                    color = tuple([int((1+border) * c) for c in color])
                yield color
        else:
            for x, y in xy_gener (width, height, resize):
                color = str_to_rgb(self.diagram[(x,y)][1])
                if self.is_border(x, y):
                    color = tuple([int(c + (border * (255-c))) for c in color])
                yield color
    
    def is_node(self, x, y, nodename):
        return self.diagram[(x,y)][0] == nodename
    
    def is_border(self, x, y):
        for dx, dy in [(0,1), (0,-1), (1,0), (-1,0)]:
            try:
                if self.diagram[(x,y)][0] != self.diagram[(x+dx,y+dy)][0]:
                    return True
            except KeyError: pass
        return False
    
    def is_coast(self, x, y):
        for dx, dy in [(0,1), (0,-1), (1,0), (-1,0)]:
            try:
                if self.diagram[(x,y)][0] != self.diagram[(x+dx,y+dy)][0]:
                    if self.is_buildable(x, y) and not self.is_buildable(x+dx, y+dy):
                        return True
                    if not self.is_buildable(x, y) and self.is_buildable(x+dx, y+dy):
                        return True
            except KeyError: pass
        return False

    def is_river(self, x, y):
        base,ship,build,cost = self.get_terrparams(x, y)
        if float(build) != 0.0 and base < 1.0: return True
        else: return False
        
    def is_buildable(self, x, y):
        base,ship,build,cost = self.get_terrparams(x, y)
        if float(build) == 0.0: return False
        else: return True
    
    def get_terrparams(self, x, y):
        color = self.diagram[(x, y)][1]
        return self.terrdict[color]


            
