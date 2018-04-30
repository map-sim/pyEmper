#! /usr/bin/python3

# author: Krzysztof Czarnecki
# email: czarnecki.krzysiek@gmail.com
# application: EMPER simulator
# brief: economic and strategic simulator
# opensource licence: GPL-3.0

import sys, os
import sqlite3

from tools import print_info
from tools import print_error

class EmperSQL:

    def __init__(self, fname):
        
        if not os.path.exists(fname):
            print_error("path %s not exists!" % fname)
            raise ValueError("database not exists")

        self.conn = sqlite3.connect(fname)
        print_info("database: %s" % fname)
        self.cur = self.conn.cursor()
        self.diagram = {}

        width = int(self.get_parameter("width"))
        height = int(self.get_parameter("height"))
        print_info("size: %d x %d" % (width, height))
        
    def __del__(self):
        self.conn.commit()
        self.conn.close()
        print_info("database closed")
        
    def execute(self, query):
        self.cur.execute(query)

    def select_row(self, query, number=0):
        self.cur.execute("%s LIMIT 1 OFFSET %d" % (query, number))
        return self.cur.fetchone()
    
    def get_nodename(self, number):
        query = "SELECT name FROM nodes LIMIT 1 OFFSET %d" % int(number)
        self.cur.execute(query)
        return self.cur.fetchone()[0]

    def select_node(self, node):
        try:
            nodename = self.get_nodename(int(node))
        except ValueError:
            nodename = node
            
        query = "SELECT * FROM nodes WHERE name='%s'" % node
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

    def get_terrdict(self):
        query = "SELECT color,conduct1,conduct2 FROM terrains"
        self.cur.execute(query)
        raw = self.cur.fetchall()

        out = {}
        for color,c1,c2 in raw:
            out[color] = (c1, c2)
        return out

    def enable_diagram(self):
        self.diagram = {}
        query = "SELECT * FROM atoms"
        for x,y,n,c in self.select_many(query):
            self.diagram[(x,y)] = (n,c)
        print_info("diagram loaded")

    def calc_points(self, nodename):
        g = self.xynode_generator(nodename)
        return len(tuple(g))
    
    def xynode_generator(self, nodename):
        for x,y in self.diagram.keys():
            if self.is_node(x, y, nodename):
                yield x,y
    
    def is_node(self, x, y, nodename):
        return self.diagram[(x,y)][0] == nodename
    
    def is_border(self, x, y):
        for dx, dy in [(0,1), (0,-1), (1,0), (-1,0)]:
            try:
                if self.diagram[(x,y)][0] != self.diagram[(x+dx,y+dy)][0]:
                    return True
            except KeyError: pass
        return False

    def is_buildable(self, x, y):
        color = self.diagram[(x,y)][1]        
        query = "SELECT conduct1 FROM terrains WHERE color='%s'" % color
        self.cur.execute(query)
        ter = self.cur.fetchone()
        if float(ter[0]) == 0.0:
            return False
        else: return True
    

