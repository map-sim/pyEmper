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
        
    def __del__(self):
        print_info("database closed")
        self.conn.commit()
        self.conn.close()
        
    def execute(self, query):
        self.cur.execute(query)
        
    def select_points(self, nodename):
        query = "SELECT x,y FROM atoms WHERE node='%s'" % str(nodename)
        self.cur.execute(query)
        return self.cur.fetchall()

    def get_node_name(self, number):
        query = "SELECT name FROM nodes LIMIT 1 OFFSET %d" % int(number)
        self.cur.execute(query)
        return self.cur.fetchone()[0]
    
    def select_row(self, query, number):        
        self.cur.execute("%s LIMIT 1 OFFSET %d" % (query, number))
        return self.cur.fetchone()

    def select_node(self, node):
        try:
            query = "SELECT * FROM nodes"
            return self.select_row(self, query, int(node))
        except ValueError:            
            query = "SELECT * FROM nodes WHERE name='%s'" % node
            self.cur.execute(query)
            return self.cur.fetchone()

    def commit(self):
        self.conn.commit()

    def enable_diagram(self):
        self.diagram = {}
        query = "SELECT * FROM atoms"
        for x,y,n,c in self.select_many(query):
            self.diagram[(x,y)] = (n,c)

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
    
    def select_many(self, query):
        self.cur.execute(query)
        return self.cur.fetchall()

    def get_parameter(self, name):
        query = "SELECT value FROM parameters WHERE name='%s'" % name 
        self.cur.execute(query)
        return self.cur.fetchone()[0]

