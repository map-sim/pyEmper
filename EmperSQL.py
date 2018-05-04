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

from AutoDicts import TerrainAutoDict
from AutoDicts import DiagramAutoDict

    
class EmperSQL(NodeDictFactory):

    def __init__(self, fname):
        
        if not os.path.exists(fname):
            print_error("path %s not exists!" % fname)
            raise ValueError("database not exists")

        self.conn = sqlite3.connect(fname)
        print_info("database: %s" % fname)
        self.cur = self.conn.cursor()

        width = int(self.get_parameter("width"))
        height = int(self.get_parameter("height"))
        print_info("size: %d x %d" % (width, height))
        
        self.terrdict = TerrainAutoDict(self.cur)
        self.diagram = DiagramAutoDict(self.cur)
        
    def __del__(self):
        self.conn.commit()
        self.conn.close()
        print_info("database closed")
        
    def execute(self, query):
        self.cur.execute(query)
            
    def select_row(self, query, number=0):
        self.cur.execute("%s LIMIT 1 OFFSET %d" % (query, number))
        return self.cur.fetchone()
    
    def get_node_name(self, number):
        query = "SELECT name FROM nodes LIMIT 1 OFFSET %d" % int(number)
        self.cur.execute(query)
        return self.cur.fetchone()[0]
    
    def get_nation_name(self, number):
        query = "SELECT name FROM nations LIMIT 1 OFFSET %d" % int(number)
        self.cur.execute(query)
        return self.cur.fetchone()[0]


    
    def select_node(self, node, columns="*"):
        query = "SELECT %s FROM nodes WHERE name='%s'" % (columns, node)
        self.cur.execute(query)
        return self.cur.fetchone()

    def select_many(self, query):
        self.cur.execute(query)
        return self.cur.fetchall()

    def get_parameter(self, name):
        query = "SELECT value FROM parameters WHERE name='%s'" % name 
        self.cur.execute(query)
        return self.cur.fetchone()[0]
    
    def commit(self):
        self.conn.commit()

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
        c1, c2, i3 = self.get_terrparams(x, y)
        if float(c1) > 0.75: return True
        else: return False
        
    def is_buildable(self, x, y):
        c1, c2, i3 = self.get_terrparams(x, y)
        if float(c1) == 0.0: return False
        else: return True
    
    def get_terrparams(self, x, y):
        color = self.diagram[(x, y)][1]
        return self.terrdict[color]


    def get_common_points(self, startname, stopname):
        commonpoints = set()
        for x,y in self.nodepoints_generator(stopname):    
            for dx,dy in [(0,1), (0,-1), (1,0), (-1,0)]:
                try:
                    if self.is_node(x+dx, y+dy, startname):
                        commonpoints.add((x+dx, y+dy))
                except KeyError: continue
        return commonpoints
            
    def calc_transit(self, startname, proxyname, stopname):
        infra_transport = self.select_node(proxyname, "infra_transport")[0]
        infra_transship = self.select_node(proxyname, "infra_transship")[0]
        world_transport = self.get_parameter("transport")
        world_transship = self.get_parameter("transship")
        world_scale =  self.get_parameter("scale")

        startpoints = self.get_common_points(startname, proxyname)
        stoppoints = self.get_common_points(proxyname, stopname)
		
        plazma = {}
        active = set()	
        for xy in startpoints:
            plazma[xy] = (1.0, None)
            active.add(xy)
	
        while active:
            try: xy = active.pop()
            except KeyError: break
	
            for dx,dy in [(0,1), (0,-1), (1,0), (-1,0)]:
                x, y = xy[0] + dx, xy[1] + dy
	        
                try:
                    
                    if self.diagram[(x, y)][0] != proxyname and \
                       self.diagram[xy][0] != proxyname:
                        continue

                    elif self.is_buildable(*xy) and self.is_buildable(x, y):   
                        c1, c2, i3 = self.get_terrparams(x, y)
                        np = plazma[xy][0] * (c1 + c2 * world_transport * i3 * infra_transport)

                        if self.is_river(x, y) and not self.is_river(*xy) or \
                           not self.is_river(x, y) and self.is_river(*xy):
                            np *= world_transship * i3 * infra_transship

                    elif not self.is_buildable(*xy) and self.is_buildable(x, y):	                
                        c1, c2, i3 = self.get_terrparams(x, y)
                        np = plazma[xy][0] * (c1  + c2 * world_transport * i3 * infra_transport)                
                        np *= world_transship * i3 * infra_transship

                    elif self.is_buildable(*xy) and not self.is_buildable(x, y):
                        c1, c2, i3 = self.get_terrparams(*xy)
                        np = plazma[xy][0] * c2 * world_transport
                        c1, c2, i3 = self.get_terrparams(x, y)
                        np *= world_transship * i3 * infra_transship
                        
                    else:
                        c1, c2, i3 = self.get_terrparams(x, y)
                        np = plazma[xy][0] * c2 * world_transport
	
                    if not (x, y) in plazma.keys():
                        plazma[(x, y)] = (0.0, None) 
	
                    if np > plazma[(x, y)][0]:
                        plazma[(x, y)] = (np, xy)                    
                        active.add((x, y))

                except KeyError: continue
	
        output = 0.0
        for xy in stoppoints:
            if not xy in plazma.keys():
                break
	
            while plazma[xy][1]:
                output += -math.log10(plazma[xy][0])
                xy = plazma[xy][1]
	
        try:
            return world_scale * output / len(stoppoints)
        except ZeroDivisionError:
            return float("inf")
